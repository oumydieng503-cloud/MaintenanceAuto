from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from garage.models import Profil, Vehicule, RendezVous, Piece, Intervention, Facture


class InscriptionTest(APITestCase):
    def test_inscription_client_ok(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'client1',
            'password': 'Test@1234',
            'role': 'client',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='client1').exists())
        self.assertEqual(Profil.objects.get(user__username='client1').role, 'client')

    def test_inscription_admin_refusee(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'hacker',
            'password': 'Test@1234',
            'role': 'administrateur',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(User.objects.filter(username='hacker').exists())

    def test_inscription_mecanicien_refusee(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'meca1',
            'password': 'Test@1234',
            'role': 'mecanicien',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StaffCreationTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='Admin@123')
        Profil.objects.create(user=self.admin, role='administrateur')
        self.client.force_authenticate(user=self.admin)

    def test_admin_cree_mecanicien(self):
        response = self.client.post('/api/auth/creer-staff/', {
            'username': 'meca1',
            'password': 'Meca@1234',
            'role': 'mecanicien',
            'email': 'meca@test.com',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profil.objects.get(user__username='meca1').role, 'mecanicien')


class ProfilMeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client1', password='Test@1234')
        Profil.objects.create(user=self.user, role='client')
        self.client.force_authenticate(user=self.user)

    def test_profil_me(self):
        response = self.client.get('/api/profils/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'client')
        self.assertEqual(response.data['user']['username'], 'client1')


class PieceAccessTest(APITestCase):
    def setUp(self):
        self.mecanicien = User.objects.create_user(username='meca', password='Meca@1234')
        Profil.objects.create(user=self.mecanicien, role='mecanicien')
        Piece.objects.create(nom='Filtre', reference='FIL-001', prix_unitaire=5000, stock=10)

    def test_mecanicien_peut_lire_pieces(self):
        self.client.force_authenticate(user=self.mecanicien)
        response = self.client.get('/api/pieces/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mecanicien_ne_peut_pas_creer_piece(self):
        self.client.force_authenticate(user=self.mecanicien)
        response = self.client.post('/api/pieces/', {
            'nom': 'Pneu',
            'reference': 'PN-001',
            'prix_unitaire': 45000,
            'stock': 5,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FactureServiceTest(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client', password='Test@1234')
        Profil.objects.create(user=self.client_user, role='client')
        self.mecanicien = User.objects.create_user(username='meca', password='Meca@1234')
        Profil.objects.create(user=self.mecanicien, role='mecanicien')

        self.vehicule = Vehicule.objects.create(
            proprietaire=self.client_user,
            marque='Toyota',
            modele='Corolla',
            immatriculation='DK-1234-AB',
            annee=2020,
            kilometrage=50000,
        )
        self.rdv = RendezVous.objects.create(
            client=self.client_user,
            vehicule=self.vehicule,
            date='2026-06-25T10:00:00Z',
            motif='Révision',
            statut='confirme',
        )
        self.intervention = Intervention.objects.create(
            rendezvous=self.rdv,
            mecanicien=self.mecanicien,
            description='Vidange moteur',
            date_debut='2026-06-25T11:00:00Z',
        )

    def test_generer_facture_intervention(self):
        from garage.services import creer_facture_pour_intervention
        facture = creer_facture_pour_intervention(self.intervention)
        self.assertIsInstance(facture, Facture)
        self.assertEqual(facture.intervention_id, self.intervention.id)
