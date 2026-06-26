# Guide de présentation — MaintenanceAuto

## Déroulé recommandé (15 minutes)

### 1. Introduction (2 min)
- Présenter le projet : gestion de garage automobile
- Stack : Django REST + JWT + MySQL + frontend HTML/JS
- 3 rôles : Client, Mécanicien, Administrateur

### 2. Architecture (2 min)
- Montrer `docs/CONCEPTION.md` — schéma BDD
- Expliquer : Frontend → API REST → Services → Models → MySQL
- Montrer Swagger : http://127.0.0.1:8000/api/docs/

### 3. Démo live (8 min)

| Étape | Compte | Action |
|-------|--------|--------|
| 1 | `admin` | Dashboard, créer mécanicien, ajouter pièces stock |
| 2 | `/inscription/` | Nouveau client → redirection auto |
| 3 | `client1` | Véhicule + RDV |
| 4 | `meca1` | Confirmer RDV → intervention → ajouter pièces → terminer |
| 5 | `admin` | Marquer facture payée |
| 6 | `client1` | Consulter facture |

### 4. Choix techniques (2 min)
- **JWT** : API stateless, réutilisable (mobile futur)
- **Couche services** : logique métier séparée des vues
- **Permissions par rôle** : sécurité granulaire
- **Swagger** : documentation vivante

### 5. Questions jury (1 min)
- Voir `docs/ANALYSE.md` pour les règles métier

---

## Avant la soutenance

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## Comptes de démo

| Rôle | Login | Mot de passe |
|------|-------|--------------|
| Admin | admin | Admin@123 |
| Mécanicien | meca1 | Meca@1234 |
| Client | client1 | Client@123 |

## Lien GitHub + Discord

Envoyer le lien du dépôt sur le canal Discord **avant le jour J**.

```bash
git remote add origin https://github.com/VOTRE_USERNAME/MaintenanceAuto.git
git push -u origin main
```
