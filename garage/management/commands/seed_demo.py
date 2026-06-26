from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from garage.models import Profil, Piece


class Command(BaseCommand):
    help = 'Charge les comptes et données de démonstration pour la soutenance'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@maintenanceauto.sn',
                'first_name': 'Super',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password('Admin@123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin créé : admin / Admin@123'))
        else:
            admin.set_password('Admin@123')
            admin.save()
            self.stdout.write('Admin mis à jour : admin / Admin@123')

        Profil.objects.update_or_create(
            user=admin,
            defaults={'role': 'administrateur', 'telephone': '771000001'},
        )

        meca, created = User.objects.get_or_create(
            username='meca1',
            defaults={
                'email': 'meca@maintenanceauto.sn',
                'first_name': 'Ali',
                'last_name': 'Fall',
            },
        )
        if created:
            meca.set_password('Meca@1234')
            meca.save()
            self.stdout.write(self.style.SUCCESS('Mécanicien créé : meca1 / Meca@1234'))
        else:
            meca.set_password('Meca@1234')
            meca.save()

        Profil.objects.update_or_create(
            user=meca,
            defaults={'role': 'mecanicien', 'telephone': '772000002'},
        )

        client, created = User.objects.get_or_create(
            username='client1',
            defaults={
                'email': 'client@maintenanceauto.sn',
                'first_name': 'Fatou',
                'last_name': 'Diop',
            },
        )
        if created:
            client.set_password('Client@123')
            client.save()
            self.stdout.write(self.style.SUCCESS('Client créé : client1 / Client@123'))
        else:
            client.set_password('Client@123')
            client.save()

        Profil.objects.update_or_create(
            user=client,
            defaults={'role': 'client', 'telephone': '773000003'},
        )

        pieces = [
            ('Filtre à huile', 'FIL-001', Decimal('8000'), 20),
            ('Plaquettes de frein', 'PLA-002', Decimal('35000'), 10),
            ('Bougie d\'allumage', 'BOU-003', Decimal('5000'), 15),
        ]
        for nom, ref, prix, stock in pieces:
            Piece.objects.update_or_create(
                reference=ref,
                defaults={'nom': nom, 'prix_unitaire': prix, 'stock': stock},
            )

        self.stdout.write(self.style.SUCCESS('Données de démonstration chargées avec succès.'))
