from django import forms
from .models import Investissement, Categorie


class InvestissementForm(forms.ModelForm):
    class Meta:
        model = Investissement
        fields = ['nom', 'categorie', 'prix_achat', 'quantite', 'date_acquisition',
                  'prix_marche', 'dividende', 'notes']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Bitcoin, LVMH, Appart Paris...'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'prix_achat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'date_acquisition': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prix_marche': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dividende': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'nom': 'Nom de l\'actif',
            'categorie': 'Catégorie',
            'prix_achat': 'Prix d\'achat unitaire (€)',
            'quantite': 'Quantité',
            'date_acquisition': 'Date d\'acquisition',
            'prix_marche': 'Prix actuel du marché (€)',
            'dividende': 'Dividende annuel par unité (€)',
            'notes': 'Notes',
        }


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'icone', 'couleur']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'icone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'bi-graph-up'}),
            'couleur': forms.Select(
                attrs={'class': 'form-select'},
                choices=[
                    ('primary', 'Bleu (primary)'),
                    ('success', 'Vert (success)'),
                    ('warning', 'Jaune (warning)'),
                    ('danger', 'Rouge (danger)'),
                    ('info', 'Cyan (info)'),
                    ('secondary', 'Gris (secondary)'),
                ]
            ),
        }
