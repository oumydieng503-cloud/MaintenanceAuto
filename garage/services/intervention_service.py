from django.utils import timezone

from garage.models import Intervention, LigneIntervention, Piece
from garage.services.facture_service import creer_facture_pour_intervention


def ajouter_piece_a_intervention(intervention, piece, quantite):
    if quantite <= 0:
        raise ValueError("La quantité doit être positive.")

    if piece.stock < quantite:
        raise ValueError(f"Stock insuffisant. Stock disponible : {piece.stock}")

    ligne = LigneIntervention.objects.create(
        intervention=intervention,
        piece=piece,
        quantite=quantite,
        prix_applique=piece.prix_unitaire,
    )

    piece.stock -= quantite
    piece.save(update_fields=['stock'])

    if hasattr(intervention, 'facture'):
        intervention.facture.calculer_montant()

    return ligne


def terminer_intervention(intervention):
    if not intervention.date_fin:
        intervention.date_fin = timezone.now()
        intervention.save(update_fields=['date_fin'])

    rendezvous = intervention.rendezvous
    if rendezvous.statut != 'termine':
        rendezvous.statut = 'termine'
        rendezvous.save(update_fields=['statut'])

    return creer_facture_pour_intervention(intervention)
