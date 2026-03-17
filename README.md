# 🏦 Asset Manager Pro

Plateforme de suivi de portefeuille financier — Django 5 + Python 3

---

## 🚀 Lancement en 5 étapes

### 1. Prérequis
```bash
python --version   # Python 3.10+ requis
```

### 2. Créer et activer un environnement virtuel
```bash
# Dans le dossier asset_manager_pro/
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Initialiser la base de données
```bash
python manage.py migrate
python manage.py seed_data       # Données de démo + compte demo/demo1234
```

### 5. Lancer le serveur
```bash
python manage.py runserver
```

Ouvrir → **http://127.0.0.1:8000**

Connexion démo : **demo / demo1234**

---

## 🗂️ Structure du projet

```
asset_manager_pro/
├── manage.py
├── requirements.txt
├── moteur.py                        ← Étape 1 : POO (Actif, Action, Portefeuille)
│
├── asset_manager/                   ← Config Django
│   ├── settings.py
│   └── urls.py
│
└── portfolio/                       ← Application principale
    ├── models.py                    ← Étape 2 : Categorie, Investissement
    ├── views.py                     ← Étapes 3 & 4 : Dashboard, API, CSV, PDF
    ├── forms.py
    ├── urls.py
    ├── admin.py
    ├── management/commands/
    │   └── seed_data.py             ← Données de démo
    └── templates/portfolio/
        ├── base.html
        ├── login.html
        ├── dashboard.html
        ├── form_investissement.html
        ├── categories.html
        └── confirmer_suppression.html
```

---

## 🌐 URLs disponibles

| URL | Description |
|-----|-------------|
| `/` | Dashboard principal |
| `/ajouter/` | Ajouter un actif |
| `/modifier/<id>/` | Modifier un actif |
| `/supprimer/<id>/` | Supprimer un actif |
| `/categories/` | Gérer les catégories |
| `/api/actifs/` | **API JSON** (Étape 4) |
| `/export/csv/` | **Export CSV** (Étape 4) |
| `/export/pdf/` | **Rapport PDF** (Étape 4) |
| `/admin/` | Interface d'administration Django |

---

## 🎓 Correspondance Étapes du projet

| Étape | Fichier | Contenu |
|-------|---------|---------|
| 1 — POO | `moteur.py` | Classes `Actif`, `Action`, `Portefeuille` |
| 2 — Models | `portfolio/models.py` | `Categorie`, `Investissement` (ORM Django) |
| 3 — Dashboard | `portfolio/views.py` + templates | KPIs, tableau, graphique, indicateurs ↑↓ |
| 4 — API/Export | `portfolio/views.py` | JSON API, CSV, PDF |

---

## 🧪 Tester le moteur Python seul (Étape 1)

```bash
python moteur.py
```
