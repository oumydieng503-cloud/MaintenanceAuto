from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('client', 'Client'),
    ('mecanicien', 'Mécanicien'),
    ('administrateur', 'Administrateur'),
]


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Vehicule(models.Model):
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicules')
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    immatriculation = models.CharField(max_length=20, unique=True)
    annee = models.IntegerField()
    kilometrage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.immatriculation}"


class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rendezvous')
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    date = models.DateTimeField()
    motif = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"RDV {self.client.username} - {self.date}"


class Intervention(models.Model):
    rendezvous = models.OneToOneField(RendezVous, on_delete=models.CASCADE)
    mecanicien = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interventions')
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Intervention {self.id} - {self.rendezvous}"


class Piece(models.Model):
    nom = models.CharField(max_length=100)
    reference = models.CharField(max_length=50, unique=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nom} ({self.reference})"


class LigneIntervention(models.Model):
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE, related_name='lignes')
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_applique = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.piece.nom} x{self.quantite}"


class Facture(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]
    intervention = models.OneToOneField(Intervention, on_delete=models.CASCADE)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_emission = models.DateTimeField(auto_now_add=True)
    statut_paiement = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def calculer_montant(self):
        total = sum(
            ligne.quantite * ligne.prix_applique
            for ligne in self.intervention.lignes.all()
        )
        self.montant_total = total
        self.save()
        return total

    def __str__(self):
        return f"Facture {self.id} - {self.montant_total} FCFA"
