"""
Étapes 3 & 4 : Vues Django — Dashboard, CRUD, API JSON, Export CSV & PDF
"""

import csv
import json
from decimal import Decimal
from collections import defaultdict
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, F
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Investissement, Categorie
from .forms import InvestissementForm, CategorieForm


# ──────────────────────────────────────────────
# Auth
# ──────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'portfolio/login.html', {'form': form})


# ──────────────────────────────────────────────
# Étape 3 — Dashboard
# ──────────────────────────────────────────────

@login_required
def dashboard(request):
    investissements = Investissement.objects.filter(utilisateur=request.user).select_related('categorie')

    # Somme totale investie (prix d'achat)
    total_investi = sum(inv.valeur_achat() for inv in investissements) or Decimal('0')
    # Valeur actuelle totale
    total_actuel = sum(inv.valeur_actuelle() for inv in investissements) or Decimal('0')
    # Plus-value globale
    plus_value_totale = total_actuel - total_investi
    performance_globale = float(plus_value_totale / total_investi * 100) if total_investi else 0.0

    # Répartition par catégorie
    repartition = defaultdict(lambda: {'valeur': Decimal('0'), 'categorie': None})
    for inv in investissements:
        cat = inv.categorie.nom
        repartition[cat]['valeur'] += inv.valeur_actuelle()
        repartition[cat]['categorie'] = inv.categorie

    repartition_liste = []
    for nom, data in repartition.items():
        pct = float(data['valeur'] / total_actuel * 100) if total_actuel else 0
        repartition_liste.append({
            'nom': nom,
            'valeur': data['valeur'],
            'pct': round(pct, 1),
            'categorie': data['categorie'],
        })
    repartition_liste.sort(key=lambda x: x['valeur'], reverse=True)

    context = {
        'investissements': investissements,
        'total_investi': total_investi,
        'total_actuel': total_actuel,
        'plus_value_totale': plus_value_totale,
        'performance_globale': performance_globale,
        'repartition': repartition_liste,
        'nb_actifs': investissements.count(),
    }
    return render(request, 'portfolio/dashboard.html', context)


# ──────────────────────────────────────────────
# CRUD Investissements
# ──────────────────────────────────────────────

@login_required
def ajouter_investissement(request):
    if request.method == 'POST':
        form = InvestissementForm(request.POST)
        if form.is_valid():
            inv = form.save(commit=False)
            inv.utilisateur = request.user
            inv.save()
            messages.success(request, f'✅ {inv.nom} ajouté avec succès !')
            return redirect('dashboard')
    else:
        form = InvestissementForm()
    return render(request, 'portfolio/form_investissement.html', {'form': form, 'titre': 'Ajouter un actif'})


@login_required
def modifier_investissement(request, pk):
    inv = get_object_or_404(Investissement, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        form = InvestissementForm(request.POST, instance=inv)
        if form.is_valid():
            form.save()
            messages.success(request, f'✏️ {inv.nom} mis à jour !')
            return redirect('dashboard')
    else:
        form = InvestissementForm(instance=inv)
    return render(request, 'portfolio/form_investissement.html', {'form': form, 'titre': f'Modifier — {inv.nom}'})


@login_required
def supprimer_investissement(request, pk):
    inv = get_object_or_404(Investissement, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        nom = inv.nom
        inv.delete()
        messages.warning(request, f'🗑️ {nom} supprimé.')
        return redirect('dashboard')
    return render(request, 'portfolio/confirmer_suppression.html', {'inv': inv})


# ──────────────────────────────────────────────
# Gestion Catégories
# ──────────────────────────────────────────────

@login_required
def gerer_categories(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Catégorie créée !')
            return redirect('categories')
    else:
        form = CategorieForm()
    categories = Categorie.objects.all()
    return render(request, 'portfolio/categories.html', {'form': form, 'categories': categories})


@login_required
def supprimer_categorie(request, pk):
    cat = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        try:
            cat.delete()
            messages.warning(request, f'🗑️ Catégorie "{cat.nom}" supprimée.')
        except Exception:
            messages.error(request, '❌ Impossible : des investissements utilisent cette catégorie.')
        return redirect('categories')
    return render(request, 'portfolio/confirmer_suppression_cat.html', {'cat': cat})


# ──────────────────────────────────────────────
# Étape 4 — API JSON
# ──────────────────────────────────────────────

@login_required
def api_actifs(request):
    """Vue API : retourne la liste des actifs au format JSON."""
    investissements = Investissement.objects.filter(utilisateur=request.user).select_related('categorie')
    data = []
    for inv in investissements:
        data.append({
            'id': inv.pk,
            'nom': inv.nom,
            'categorie': inv.categorie.nom,
            'prix_achat': float(inv.prix_achat),
            'quantite': inv.quantite,
            'valeur_achat': float(inv.valeur_achat()),
            'prix_marche': float(inv.prix_marche) if inv.prix_marche else None,
            'valeur_actuelle': float(inv.valeur_actuelle()),
            'performance_pct': round(inv.performance(), 2),
            'plus_value': float(inv.plus_value()),
            'dividende': float(inv.dividende),
            'rendement_annuel_pct': round(inv.rendement_annuel(), 2),
            'date_acquisition': str(inv.date_acquisition),
        })
    return JsonResponse({'actifs': data, 'total': len(data)}, json_dumps_params={'ensure_ascii': False})


# ──────────────────────────────────────────────
# Export CSV
# ──────────────────────────────────────────────

@login_required
def export_csv(request):
    """Exporte les investissements en CSV (téléchargement direct)."""
    investissements = Investissement.objects.filter(utilisateur=request.user).select_related('categorie')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="portefeuille.csv"'
    response.write('\ufeff')  # BOM pour Excel

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Nom', 'Catégorie', 'Date acquisition', 'Prix achat (€)',
        'Quantité', 'Valeur achat (€)', 'Prix marché (€)',
        'Valeur actuelle (€)', 'Performance (%)', 'Plus-value (€)',
        'Dividende/an (€)', 'Rendement (%)', 'Notes'
    ])
    for inv in investissements:
        writer.writerow([
            inv.nom, inv.categorie.nom, inv.date_acquisition,
            inv.prix_achat, inv.quantite,
            round(inv.valeur_achat(), 2),
            inv.prix_marche or '',
            round(inv.valeur_actuelle(), 2),
            round(inv.performance(), 2),
            round(inv.plus_value(), 2),
            inv.dividende,
            round(inv.rendement_annuel(), 2),
            inv.notes,
        ])
    return response


# ──────────────────────────────────────────────
# Export PDF
# ──────────────────────────────────────────────

@login_required
def export_pdf(request):
    """Génère un rapport PDF de synthèse du portefeuille."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.units import cm
        from reportlab.lib.enums import TA_CENTER
    except ImportError:
        return HttpResponse("ReportLab non installé. Lancez : pip install reportlab", status=500)

    investissements = Investissement.objects.filter(utilisateur=request.user).select_related('categorie')
    total_investi = sum(inv.valeur_achat() for inv in investissements) or Decimal('0')
    total_actuel = sum(inv.valeur_actuelle() for inv in investissements) or Decimal('0')
    plus_value = total_actuel - total_investi

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    titre_style = ParagraphStyle('Titre', parent=styles['Title'], fontSize=18, textColor=colors.HexColor('#1a1a2e'))
    sous_titre_style = ParagraphStyle('SousTitre', parent=styles['Normal'], fontSize=10,
                                       textColor=colors.grey, alignment=TA_CENTER)

    elements = []
    elements.append(Paragraph("Asset Manager Pro", titre_style))
    elements.append(Paragraph(f"Rapport de portefeuille — {request.user.get_full_name() or request.user.username}", sous_titre_style))
    elements.append(Spacer(1, 0.5*cm))

    # Résumé
    resume_data = [
        ['Total investi', f"{total_investi:,.2f} €"],
        ['Valeur actuelle', f"{total_actuel:,.2f} €"],
        ['Plus-value', f"{plus_value:,.2f} €"],
        ['Nombre d\'actifs', str(investissements.count())],
    ]
    resume_table = Table(resume_data, colWidths=[6*cm, 6*cm])
    resume_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f4ff')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')]),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(resume_table)
    elements.append(Spacer(1, 0.7*cm))

    # Tableau des actifs
    elements.append(Paragraph("Détail des investissements", styles['Heading2']))
    elements.append(Spacer(1, 0.3*cm))

    headers = ['Actif', 'Catégorie', 'Qté', 'Prix achat', 'Valeur achat', 'Valeur act.', 'Perf. %']
    rows = [headers]
    for inv in investissements:
        perf = inv.performance()
        rows.append([
            inv.nom[:25],
            inv.categorie.nom,
            str(inv.quantite),
            f"{inv.prix_achat:,.2f} €",
            f"{inv.valeur_achat():,.2f} €",
            f"{inv.valeur_actuelle():,.2f} €",
            f"{perf:+.1f}%",
        ])

    col_widths = [4.5*cm, 3*cm, 1.5*cm, 2.5*cm, 3*cm, 3*cm, 2*cm]
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9ff')]),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_portefeuille.pdf"'
    return response
