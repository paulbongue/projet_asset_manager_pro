"""
Étape 2 : Persistance des données (Django Models)
"""

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Categorie(models.Model):
    """Catégorie d'investissement : Bourse, Crypto, Immobilier, Épargne..."""
    nom = models.CharField(max_length=100, unique=True)
    icone = models.CharField(
        max_length=50, default='bi-briefcase',
        help_text="Classe Bootstrap Icon (ex: bi-graph-up, bi-currency-bitcoin)"
    )
    couleur = models.CharField(
        max_length=20, default='primary',
        help_text="Couleur Bootstrap: primary, success, warning, danger, info"
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Investissement(models.Model):
    """Actif financier appartenant à un utilisateur."""
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investissements')
    nom = models.CharField(max_length=200)
    prix_achat = models.DecimalField(max_digits=15, decimal_places=2)
    quantite = models.FloatField()
    date_acquisition = models.DateField()
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name='investissements')
    # Prix actuel du marché (simulé manuellement pour la démo)
    prix_marche = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True,
        help_text="Prix actuel sur le marché (pour calculer +/-)"
    )
    # Pour les actions : dividende annuel par unité
    dividende = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Dividende annuel par unité (actions uniquement)"
    )
    notes = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = "Investissement"
        verbose_name_plural = "Investissements"
        ordering = ['-date_acquisition']

    def valeur_achat(self) -> Decimal:
        """Valeur totale au prix d'achat."""
        return self.prix_achat * Decimal(str(self.quantite))

    def valeur_actuelle(self) -> Decimal:
        """Valeur actuelle (prix marché × quantité). Retourne valeur_achat si pas de prix marché."""
        if self.prix_marche:
            return self.prix_marche * Decimal(str(self.quantite))
        return self.valeur_achat()

    def performance(self) -> float:
        """Variation en % entre prix d'achat et prix marché."""
        if not self.prix_marche or self.prix_achat == 0:
            return 0.0
        return float((self.prix_marche - self.prix_achat) / self.prix_achat * 100)

    def plus_value(self) -> Decimal:
        """Plus-value en valeur absolue."""
        return self.valeur_actuelle() - self.valeur_achat()

    def est_en_hausse(self) -> bool:
        """Retourne True si la valeur a augmenté de plus de 10%."""
        return self.performance() > 10

    def rendement_annuel(self) -> float:
        """Rendement dividende en % (pour les actions)."""
        if self.prix_achat == 0:
            return 0.0
        return float(self.dividende / self.prix_achat * 100)

    def __str__(self):
        return f"{self.nom} ({self.categorie})"
