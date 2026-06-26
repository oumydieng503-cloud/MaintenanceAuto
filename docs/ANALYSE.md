# Analyse — MaintenanceAuto

## 1. Acteurs

| Acteur | Description | Accès |
|--------|-------------|-------|
| **Client** | Propriétaire de véhicule | Inscription publique, espace client |
| **Mécanicien** | Technicien du garage | Créé par l'admin, espace mécanicien |
| **Administrateur** | Responsable du garage | Créé manuellement ou par un admin, espace admin |

---

## 2. Cas d'utilisation

### Client
- S'inscrire et se connecter
- Ajouter / consulter ses véhicules
- Prendre un rendez-vous pour un véhicule
- Consulter ses factures

### Mécanicien
- Se connecter
- Consulter les rendez-vous
- Confirmer ou terminer un rendez-vous
- Créer une intervention liée à un RDV
- Ajouter des pièces à une intervention (décrémente le stock)
- Consulter ses propres interventions

### Administrateur
- Se connecter
- Consulter le tableau de bord (statistiques)
- Créer des comptes mécanicien et administrateur
- Gérer le stock de pièces (CRUD)
- Consulter tous les rendez-vous et factures
- Générer et marquer les factures comme payées

---

## 3. Diagramme de cas d'utilisation (texte)

```
                    ┌─────────────────────────────────────┐
                    │           MaintenanceAuto            │
                    └─────────────────────────────────────┘
         ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
         │    Client    │  │  Mécanicien  │  │ Administrateur   │
         └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
                │                 │                    │
    S'inscrire  │    Confirmer RDV│    Créer staff     │
    Ajouter     │    Intervention │    Gérer stock     │
    véhicule    │    Ajouter      │    Facturation     │
    Prendre RDV │    pièces       │    Dashboard       │
    Voir        │    Terminer RDV │                    │
    factures    │                 │                    │
```

---

## 4. Règles métier

### Authentification et rôles
| Règle | Description |
|-------|-------------|
| R1 | Seuls les **clients** peuvent s'inscrire via l'endpoint public |
| R2 | Les **mécaniciens** et **administrateurs** sont créés uniquement par un admin |
| R3 | Chaque utilisateur possède un **Profil** avec un rôle unique |
| R4 | L'authentification se fait via **JWT** (access + refresh token) |

### Véhicules
| Règle | Description |
|-------|-------------|
| R5 | Un véhicule appartient à **un seul client** |
| R6 | L'**immatriculation** doit être unique |
| R7 | Un client ne voit que **ses propres véhicules** |

### Rendez-vous
| Règle | Description |
|-------|-------------|
| R8 | Un RDV est lié à un véhicule et un client |
| R9 | Statuts possibles : `en_attente`, `confirme`, `annule`, `termine` |
| R10 | Le statut initial est **en_attente** |

### Interventions
| Règle | Description |
|-------|-------------|
| R11 | Une intervention est liée à **un seul RDV** (OneToOne) |
| R12 | Le mécanicien est **automatiquement assigné** à la création |
| R13 | Un mécanicien ne voit que **ses propres interventions** |

### Stock et pièces
| Règle | Description |
|-------|-------------|
| R14 | Seul l'**admin** peut créer/modifier/supprimer des pièces |
| R15 | Le **mécanicien** peut consulter le stock |
| R16 | L'ajout d'une pièce à une intervention **décrémente le stock** |
| R17 | Si stock insuffisant → opération **refusée** |

### Facturation
| Règle | Description |
|-------|-------------|
| R18 | Une facture est liée à **une intervention** (OneToOne) |
| R19 | Le montant = somme de `quantité × prix_applique` par ligne |
| R20 | Une facture est **générée automatiquement** quand un RDV est terminé |
| R21 | Statuts paiement : `en_attente`, `payee`, `annulee` |
| R22 | Le client ne voit que **ses propres factures** |
