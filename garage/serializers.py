from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profil, Vehicule, RendezVous, Intervention, Piece, LigneIntervention, Facture


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profil
        fields = ['id', 'user', 'role', 'telephone', 'adresse']


class VehiculeSerializer(serializers.ModelSerializer):
    proprietaire = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vehicule
        fields = ['id', 'proprietaire', 'marque', 'modele', 'immatriculation', 'annee', 'kilometrage']


class RendezVousSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    client_nom = serializers.SerializerMethodField()
    vehicule_info = serializers.SerializerMethodField()

    class Meta:
        model = RendezVous
        fields = [
            'id', 'client', 'client_nom', 'vehicule', 'vehicule_info',
            'date', 'motif', 'statut',
        ]

    def get_client_nom(self, obj):
        nom = f"{obj.client.first_name} {obj.client.last_name}".strip()
        return nom or obj.client.username

    def get_vehicule_info(self, obj):
        vehicule = obj.vehicule
        return f"{vehicule.marque} {vehicule.modele} ({vehicule.immatriculation})"


class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ['id', 'nom', 'reference', 'prix_unitaire', 'stock']


class LigneInterventionSerializer(serializers.ModelSerializer):
    piece = PieceSerializer(read_only=True)
    piece_id = serializers.PrimaryKeyRelatedField(
        queryset=Piece.objects.all(), source='piece', write_only=True
    )

    class Meta:
        model = LigneIntervention
        fields = ['id', 'piece', 'piece_id', 'quantite', 'prix_applique']


class InterventionSerializer(serializers.ModelSerializer):
    mecanicien = serializers.PrimaryKeyRelatedField(read_only=True)
    lignes = LigneInterventionSerializer(many=True, read_only=True)
    rendezvous_info = serializers.SerializerMethodField()

    class Meta:
        model = Intervention
        fields = [
            'id', 'rendezvous', 'rendezvous_info', 'mecanicien',
            'description', 'date_debut', 'date_fin', 'lignes',
        ]

    def get_rendezvous_info(self, obj):
        rdv = obj.rendezvous
        return f"RDV #{rdv.id} - {rdv.motif}"


class FactureSerializer(serializers.ModelSerializer):
    intervention_info = serializers.SerializerMethodField()

    class Meta:
        model = Facture
        fields = [
            'id', 'intervention', 'intervention_info',
            'montant_total', 'date_emission', 'statut_paiement',
        ]

    def get_intervention_info(self, obj):
        return f"Intervention #{obj.intervention_id} - {obj.intervention.description[:40]}"
