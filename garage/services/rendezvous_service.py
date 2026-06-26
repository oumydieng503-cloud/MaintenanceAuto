from garage.models import RendezVous


def changer_statut_rendezvous(rendezvous, nouveau_statut):
    statuts_valides = {choice[0] for choice in RendezVous.STATUT_CHOICES}
    if nouveau_statut not in statuts_valides:
        raise ValueError("Statut invalide.")

    rendezvous.statut = nouveau_statut
    rendezvous.save(update_fields=['statut'])

    if nouveau_statut == 'termine' and hasattr(rendezvous, 'intervention'):
        from garage.services.intervention_service import terminer_intervention
        terminer_intervention(rendezvous.intervention)

    return rendezvous
