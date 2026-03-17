"""
Commande pour peupler la base avec des données de démonstration.
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from portfolio.models import Categorie, Investissement
import datetime


class Command(BaseCommand):
    help = 'Peuple la base avec des données de démo'

    def handle(self, *args, **options):
        # Catégories
        cats = {
            'Bourse': ('bi-graph-up', 'primary'),
            'Crypto': ('bi-currency-bitcoin', 'warning'),
            'Immobilier': ('bi-house', 'success'),
            'Épargne': ('bi-piggy-bank', 'info'),
        }
        cat_objects = {}
        for nom, (icone, couleur) in cats.items():
            cat, _ = Categorie.objects.get_or_create(nom=nom, defaults={'icone': icone, 'couleur': couleur})
            cat_objects[nom] = cat
            self.stdout.write(f'  ✅ Catégorie : {nom}')

        # Utilisateur demo
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={'first_name': 'Jean', 'last_name': 'Dupont', 'email': 'demo@example.com'}
        )
        if created:
            user.set_password('demo1234')
            user.save()
            self.stdout.write('  ✅ Utilisateur demo créé (mot de passe : demo1234)')
        else:
            self.stdout.write('  ℹ️  Utilisateur demo existe déjà')

        # Investissements de démo
        actifs = [
            ('LVMH', cat_objects['Bourse'], 750, 10, '2023-01-15', 820, 12),
            ('TotalEnergies', cat_objects['Bourse'], 55, 50, '2022-06-10', 60, 3),
            ('Bitcoin', cat_objects['Crypto'], 35000, 0.5, '2021-11-01', 62000, 0),
            ('Ethereum', cat_objects['Crypto'], 2000, 2, '2022-03-20', 3200, 0),
            ('Appartement Lyon', cat_objects['Immobilier'], 220000, 1, '2020-09-01', 245000, 0),
            ('Livret A', cat_objects['Épargne'], 10000, 1, '2023-01-01', 10300, 0),
            ('Air Liquide', cat_objects['Bourse'], 145, 20, '2023-05-12', 158, 2.8),
        ]
        for nom, cat, prix_achat, qte, date_str, prix_marche, dividende in actifs:
            if not Investissement.objects.filter(utilisateur=user, nom=nom).exists():
                Investissement.objects.create(
                    utilisateur=user, nom=nom, categorie=cat,
                    prix_achat=prix_achat, quantite=qte,
                    date_acquisition=datetime.date.fromisoformat(date_str),
                    prix_marche=prix_marche, dividende=dividende,
                )
                self.stdout.write(f'  ✅ Actif ajouté : {nom}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Données de démo créées ! Connectez-vous avec demo / demo1234'))
