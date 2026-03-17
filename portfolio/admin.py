from django.contrib import admin
from .models import Categorie, Investissement


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'icone', 'couleur']


@admin.register(Investissement)
class InvestissementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'utilisateur', 'prix_achat', 'quantite', 'date_acquisition']
    list_filter = ['categorie', 'utilisateur']
    search_fields = ['nom']
