from django.contrib import admin

from .models import Profil, Vehicule, RendezVous, Intervention, Piece, LigneIntervention, Facture


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'telephone']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ['immatriculation', 'marque', 'modele', 'proprietaire', 'annee']
    search_fields = ['immatriculation', 'marque', 'modele']


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['client', 'vehicule', 'date', 'statut']
    list_filter = ['statut']
    search_fields = ['client__username', 'motif']


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['id', 'mecanicien', 'rendezvous', 'date_debut', 'date_fin']
    list_filter = ['date_debut']


@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'reference', 'prix_unitaire', 'stock']
    search_fields = ['nom', 'reference']


@admin.register(LigneIntervention)
class LigneInterventionAdmin(admin.ModelAdmin):
    list_display = ['intervention', 'piece', 'quantite', 'prix_applique']


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'montant_total', 'statut_paiement', 'date_emission']
    list_filter = ['statut_paiement']
