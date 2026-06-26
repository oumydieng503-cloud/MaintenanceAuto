# MaintenanceAuto

## Description

**MaintenanceAuto** est une application web de gestion de garage automobile développée dans le cadre du module Django à ISI SupTech.

Elle permet à trois types d'utilisateurs d'interagir avec le système :
- Les **clients** s'inscrivent, enregistrent leurs véhicules, prennent des rendez-vous et consultent leurs factures.
- Les **mécaniciens** traitent les rendez-vous, réalisent des interventions et utilisent les pièces du stock.
- Les **administrateurs** supervisent l'activité, gèrent le stock et la facturation.

L'application suit une architecture **API REST + frontend** : le backend Django expose une API JSON sécurisée par JWT, et le frontend HTML/JS consomme cette API via `fetch`.

Documentation complète :
- [Analyse (acteurs, cas d'utilisation, règles métier)](docs/ANALYSE.md)
- [Conception (schéma BDD, endpoints)](docs/CONCEPTION.md)

---

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Backend | Django 4.2, Django REST Framework |
| Authentification | JWT (djangorestframework-simplejwt) |
| Base de données | MySQL |
| Documentation API | drf-spectacular (Swagger UI) |
| Frontend | HTML5, Bootstrap 5, JavaScript (fetch API) |
| Configuration | python-dotenv (.env) |

---

## Installation

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd MaintenanceAuto
```

### 2. Créer l'environnement virtuel

```bash
python -m venv env
env\Scripts\activate        # Windows
# source env/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

```bash
copy .env.example .env      # Windows
# cp .env.example .env      # Linux/Mac
```

Remplir les valeurs dans `.env` (voir section ci-dessous).

### 4. Créer la base de données MySQL

```sql
CREATE DATABASE maintenanceauto CHARACTER SET utf8mb4;
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Charger les données de démonstration

```bash
python manage.py seed_demo
```

### 7. Lancer le serveur

```bash
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/

---

## Variables d'environnement

| Variable | Description | Exemple |
|----------|-------------|---------|
| `SECRET_KEY` | Clé secrète Django | `votre-cle-secrete-ici` |
| `DEBUG` | Mode debug | `True` |
| `ALLOWED_HOSTS` | Hôtes autorisés | `localhost,127.0.0.1` |
| `DB_ENGINE` | Moteur BDD | `django.db.backends.mysql` |
| `DB_NAME` | Nom de la base | `maintenanceauto` |
| `DB_USER` | Utilisateur MySQL | `root` |
| `DB_PASSWORD` | Mot de passe MySQL | *(vide sur XAMPP)* |
| `DB_HOST` | Hôte MySQL | `localhost` |
| `DB_PORT` | Port MySQL | `3306` |

> Copier `.env.example` vers `.env` et remplir les valeurs. Ne jamais committer le fichier `.env`.

---

## Endpoints API

Base : `http://127.0.0.1:8000/api/`  
Documentation interactive : http://127.0.0.1:8000/api/docs/

### Authentification

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| POST | `/auth/login/` | Non | Connexion JWT |
| POST | `/auth/refresh/` | Non | Rafraîchir le token |
| POST | `/auth/register/` | Non | Inscription client |
| POST | `/auth/creer-staff/` | Admin | Créer mécanicien/admin |

### Ressources principales

| Ressource | Endpoint | Rôles |
|-----------|----------|-------|
| Profils | `/profils/`, `/profils/me/` | Tous (filtré) |
| Véhicules | `/vehicules/` | Client, Admin |
| Rendez-vous | `/rendezvous/` | Client, Mécanicien, Admin |
| Interventions | `/interventions/` | Mécanicien, Admin |
| Pièces | `/pieces/` | Mécanicien (lecture), Admin (CRUD) |
| Factures | `/factures/` | Client (siennes), Admin (toutes) |

### Actions métier

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/interventions/{id}/ajouter-piece/` | Ajouter pièce + décrémenter stock |
| POST | `/interventions/{id}/generer-facture/` | Générer une facture |
| POST | `/factures/{id}/recalculer/` | Recalculer le montant |

Liste complète : [docs/CONCEPTION.md](docs/CONCEPTION.md)

---

## Comptes de démonstration

Créés automatiquement par `python manage.py seed_demo` :

| Rôle | Username | Mot de passe | Espace |
|------|----------|--------------|--------|
| Administrateur | `admin` | `Admin@123` | `/dashboard/admin/` |
| Mécanicien | `meca1` | `Meca@1234` | `/dashboard/mecanicien/` |
| Client | `client1` | `Client@123` | `/dashboard/client/` |

**Pièces en stock (seed)** : Filtre à huile (FIL-001), Plaquettes de frein (PLA-002)

**Inscription client** : http://127.0.0.1:8000/inscription/ (redirection automatique après inscription)

---

## Tests

```bash
python manage.py test garage
```

8 tests automatisés : inscription, sécurité des rôles, accès pièces, facturation.

---

## Auteur

Projet réalisé dans le cadre de l'examen Django — **ISI SupTech**
