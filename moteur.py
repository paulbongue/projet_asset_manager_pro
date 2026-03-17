"""
Étape 1 : Algorithmique & POO
Moteur de calcul des actifs financiers.
"""


class Actif:
    """Classe de base représentant un actif financier."""

    def __init__(self, nom: str, quantite: float, prix_unitaire: float):
        self.nom = nom
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire

    def valeur_totale(self) -> float:
        """Retourne la valeur totale de l'actif (quantité × prix unitaire)."""
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.nom} | Qté: {self.quantite} | Prix: {self.prix_unitaire:.2f} | Valeur: {self.valeur_totale():.2f}"


class Action(Actif):
    """Sous-classe d'Actif représentant une action boursière avec dividende."""

    def __init__(self, nom: str, quantite: float, prix_unitaire: float, dividende: float):
        super().__init__(nom, quantite, prix_unitaire)
        self.dividende = dividende  # dividende annuel par action (en devise)

    def rendement_annuel(self) -> float:
        """
        Calcule le rendement annuel en % basé sur le dividende par rapport au prix unitaire.
        Rendement = (dividende / prix_unitaire) × 100
        """
        if self.prix_unitaire == 0:
            return 0.0
        return (self.dividende / self.prix_unitaire) * 100

    def revenus_dividendes(self) -> float:
        """Calcule les revenus totaux en dividendes pour la quantité détenue."""
        return self.dividende * self.quantite

    def __str__(self):
        return (
            f"{super().__str__()} | "
            f"Dividende: {self.dividende:.2f} | "
            f"Rendement: {self.rendement_annuel():.2f}%"
        )


class Portefeuille:
    """Gère un ensemble d'actifs financiers."""

    def __init__(self, nom: str):
        self.nom = nom
        self.actifs: list[Actif] = []

    def ajouter_actif(self, actif: Actif):
        self.actifs.append(actif)

    def valeur_totale(self) -> float:
        return sum(a.valeur_totale() for a in self.actifs)

    def __str__(self):
        lignes = [f"=== Portefeuille : {self.nom} ==="]
        for a in self.actifs:
            lignes.append(f"  - {a}")
        lignes.append(f"  TOTAL : {self.valeur_totale():.2f}")
        return "\n".join(lignes)


# ---------------------------------------------------------------------------
# Démonstration rapide (python moteur.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    p = Portefeuille("Mon Patrimoine")
    p.ajouter_actif(Actif("Bitcoin", 0.5, 60000))
    p.ajouter_actif(Actif("Appartement Paris", 1, 320000))
    p.ajouter_actif(Action("LVMH", 10, 750, dividende=12))
    p.ajouter_actif(Action("TotalEnergies", 50, 55, dividende=3))
    print(p)
