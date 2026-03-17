from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ajouter/', views.ajouter_investissement, name='ajouter'),
    path('modifier/<int:pk>/', views.modifier_investissement, name='modifier'),
    path('supprimer/<int:pk>/', views.supprimer_investissement, name='supprimer'),
    path('categories/', views.gerer_categories, name='categories'),
    path('categories/supprimer/<int:pk>/', views.supprimer_categorie, name='supprimer_categorie'),
    # Étape 4
    path('api/actifs/', views.api_actifs, name='api_actifs'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]
