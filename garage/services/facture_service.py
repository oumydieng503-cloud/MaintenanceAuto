from garage.models import Facture, Intervention


def creer_facture_pour_intervention(intervention):
    if hasattr(intervention, 'facture'):
        return intervention.facture

    facture = Facture.objects.create(intervention=intervention, montant_total=0)
    facture.calculer_montant()
    return facture


def recalculer_facture(facture):
    return facture.calculer_montant()


def marquer_facture_payee(facture):
    facture.statut_paiement = 'payee'
    facture.save()
    return facture
