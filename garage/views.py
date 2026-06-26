from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Profil, Vehicule, RendezVous, Intervention, Piece, Facture
from .serializers import (
    UserSerializer,
    ProfilSerializer,
    VehiculeSerializer,
    RendezVousSerializer,
    InterventionSerializer,
    PieceSerializer,
    FactureSerializer,
)
from .permissions import EstAdmin, EstMecanicien, EstAdminOuMecanicien
from . import services


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, EstAdmin]


class ProfilViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profil') and user.profil.role == 'administrateur':
            return Profil.objects.select_related('user').all()
        return Profil.objects.select_related('user').filter(user=user)


@extend_schema_view(
    list=extend_schema(tags=['Véhicules'], summary='Lister les véhicules'),
    create=extend_schema(tags=['Véhicules'], summary='Ajouter un véhicule (client)'),
    retrieve=extend_schema(tags=['Véhicules'], summary='Détail d\'un véhicule'),
    update=extend_schema(tags=['Véhicules'], summary='Modifier un véhicule'),
    destroy=extend_schema(tags=['Véhicules'], summary='Supprimer un véhicule'),
)
class VehiculeViewSet(viewsets.ModelViewSet):
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profil') and user.profil.role == 'administrateur':
            return Vehicule.objects.all()
        return Vehicule.objects.filter(proprietaire=user)

    def perform_create(self, serializer):
        serializer.save(proprietaire=self.request.user)


@extend_schema_view(
    list=extend_schema(tags=['Rendez-vous'], summary='Lister les rendez-vous'),
    create=extend_schema(tags=['Rendez-vous'], summary='Prendre un rendez-vous'),
    retrieve=extend_schema(tags=['Rendez-vous'], summary='Détail d\'un rendez-vous'),
    update=extend_schema(tags=['Rendez-vous'], summary='Modifier un rendez-vous'),
    partial_update=extend_schema(tags=['Rendez-vous'], summary='Changer le statut d\'un RDV'),
    destroy=extend_schema(tags=['Rendez-vous'], summary='Supprimer un rendez-vous'),
)
class RendezVousViewSet(viewsets.ModelViewSet):
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'profil'):
            return RendezVous.objects.none()

        if user.profil.role == 'administrateur':
            return RendezVous.objects.select_related('client', 'vehicule').all()
        if user.profil.role == 'mecanicien':
            return RendezVous.objects.select_related('client', 'vehicule').all()
        return RendezVous.objects.select_related('client', 'vehicule').filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def perform_update(self, serializer):
        ancien_statut = serializer.instance.statut
        instance = serializer.save()
        nouveau_statut = serializer.validated_data.get('statut')
        if nouveau_statut and nouveau_statut != ancien_statut:
            services.changer_statut_rendezvous(instance, nouveau_statut)


@extend_schema_view(
    list=extend_schema(tags=['Interventions'], summary='Lister les interventions'),
    create=extend_schema(tags=['Interventions'], summary='Créer une intervention'),
    retrieve=extend_schema(tags=['Interventions'], summary='Détail d\'une intervention'),
    update=extend_schema(tags=['Interventions'], summary='Modifier une intervention'),
    partial_update=extend_schema(tags=['Interventions'], summary='Mettre à jour une intervention'),
    destroy=extend_schema(tags=['Interventions'], summary='Supprimer une intervention'),
)
class InterventionViewSet(viewsets.ModelViewSet):
    serializer_class = InterventionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'profil'):
            return Intervention.objects.none()

        if user.profil.role == 'administrateur':
            return Intervention.objects.select_related('rendezvous', 'mecanicien').all()
        if user.profil.role == 'mecanicien':
            return Intervention.objects.select_related('rendezvous', 'mecanicien').filter(mecanicien=user)
        return Intervention.objects.select_related('rendezvous', 'mecanicien').filter(rendezvous__client=user)

    def perform_create(self, serializer):
        intervention = serializer.save(mecanicien=self.request.user)
        if intervention.date_fin:
            services.terminer_intervention(intervention)

    def perform_update(self, serializer):
        intervention = serializer.save()
        if intervention.date_fin:
            services.terminer_intervention(intervention)


@extend_schema_view(
    list=extend_schema(tags=['Pièces'], summary='Consulter le stock de pièces'),
    create=extend_schema(tags=['Pièces'], summary='Ajouter une pièce (admin)'),
    retrieve=extend_schema(tags=['Pièces'], summary='Détail d\'une pièce'),
    update=extend_schema(tags=['Pièces'], summary='Modifier une pièce (admin)'),
    destroy=extend_schema(tags=['Pièces'], summary='Supprimer une pièce (admin)'),
)
class PieceViewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated(), EstAdminOuMecanicien()]
        return [IsAuthenticated(), EstAdmin()]


@extend_schema_view(
    list=extend_schema(tags=['Factures'], summary='Lister les factures'),
    create=extend_schema(tags=['Factures'], summary='Créer une facture (admin)'),
    retrieve=extend_schema(tags=['Factures'], summary='Détail d\'une facture'),
    update=extend_schema(tags=['Factures'], summary='Modifier une facture'),
    partial_update=extend_schema(tags=['Factures'], summary='Marquer une facture comme payée'),
    destroy=extend_schema(tags=['Factures'], summary='Supprimer une facture'),
)
class FactureViewSet(viewsets.ModelViewSet):
    serializer_class = FactureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profil') and user.profil.role == 'administrateur':
            return Facture.objects.select_related('intervention').all()
        return Facture.objects.select_related('intervention').filter(
            intervention__rendezvous__client=user
        )

    def perform_create(self, serializer):
        facture = serializer.save()
        facture.calculer_montant()

    def perform_update(self, serializer):
        facture = serializer.save()
        if facture.statut_paiement == 'payee':
            services.marquer_facture_payee(facture)


@extend_schema(
    tags=['Auth'],
    summary='Inscription client',
    description='Crée un compte client. Seul le rôle "client" est accepté. Les mécaniciens et admins sont créés via /auth/creer-staff/.',
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    role = request.data.get('role', 'client')
    if role != 'client':
        return Response(
            {'error': "Seuls les clients peuvent s'inscrire. Contactez l'administrateur pour les autres rôles."},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        user = services.inscrire_client(
            username=request.data.get('username'),
            password=request.data.get('password'),
            email=request.data.get('email', ''),
            first_name=request.data.get('first_name', ''),
            last_name=request.data.get('last_name', ''),
            telephone=request.data.get('telephone', ''),
            adresse=request.data.get('adresse', ''),
        )
    except ValueError as exc:
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {
            'message': 'Compte client créé avec succès',
            'username': user.username,
            'role': 'client',
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=['Auth'],
    summary='Créer un compte staff',
    description='Réservé à l\'administrateur. Crée un mécanicien ou un administrateur.',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, EstAdmin])
def creer_staff(request):
    role = request.data.get('role')
    if role not in ('mecanicien', 'administrateur'):
        return Response(
            {'error': "Rôle invalide. Choisissez mécanicien ou administrateur."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = services.creer_utilisateur_staff(
            admin_user=request.user,
            username=request.data.get('username'),
            password=request.data.get('password'),
            email=request.data.get('email', ''),
            first_name=request.data.get('first_name', ''),
            last_name=request.data.get('last_name', ''),
            role=role,
            telephone=request.data.get('telephone', ''),
            adresse=request.data.get('adresse', ''),
        )
    except PermissionError as exc:
        return Response({'error': str(exc)}, status=status.HTTP_403_FORBIDDEN)
    except ValueError as exc:
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {
            'message': f'Compte {role} créé avec succès',
            'username': user.username,
            'role': role,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=['Profils'],
    summary='Mon profil',
    description='Retourne le profil de l\'utilisateur connecté (rôle, téléphone, etc.).',
    responses={200: ProfilSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profil_me(request):
    try:
        profil = request.user.profil
    except Profil.DoesNotExist:
        return Response({'error': 'Profil non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    return Response(ProfilSerializer(profil).data)


@extend_schema(
    tags=['Interventions'],
    summary='Ajouter une pièce à une intervention',
    description='Ajoute une pièce au stock d\'une intervention et décrémente le stock. Mécanicien ou admin.',
    parameters=[OpenApiParameter('intervention_id', int, OpenApiParameter.PATH)],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, EstAdminOuMecanicien])
def ajouter_piece_intervention(request, intervention_id):
    try:
        intervention = Intervention.objects.get(id=intervention_id)
    except Intervention.DoesNotExist:
        return Response({'error': 'Intervention non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    if hasattr(request.user, 'profil') and request.user.profil.role == 'mecanicien':
        if intervention.mecanicien_id != request.user.id:
            return Response({'error': 'Accès refusé à cette intervention.'}, status=status.HTTP_403_FORBIDDEN)

    piece_id = request.data.get('piece_id')
    quantite = int(request.data.get('quantite', 1))

    try:
        piece = Piece.objects.get(id=piece_id)
    except (Piece.DoesNotExist, TypeError, ValueError):
        return Response({'error': 'Pièce non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    try:
        ligne = services.ajouter_piece_a_intervention(intervention, piece, quantite)
    except ValueError as exc:
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {
            'message': f'{quantite} x {piece.nom} ajouté à l\'intervention',
            'stock_restant': piece.stock,
            'prix_applique': ligne.prix_applique,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=['Factures'],
    summary='Recalculer une facture',
    description='Recalcule le montant total à partir des pièces de l\'intervention.',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, EstAdmin])
def recalculer_facture_view(request, facture_id):
    try:
        facture = Facture.objects.get(id=facture_id)
    except Facture.DoesNotExist:
        return Response({'error': 'Facture non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    montant = services.recalculer_facture(facture)
    return Response(
        {
            'message': 'Facture recalculée avec succès',
            'montant_total': montant,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=['Factures'],
    summary='Générer une facture pour une intervention',
    description='Crée ou retourne la facture liée à une intervention. Le montant est calculé automatiquement.',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, EstAdmin])
def generer_facture(request, intervention_id):
    try:
        intervention = Intervention.objects.get(id=intervention_id)
    except Intervention.DoesNotExist:
        return Response({'error': 'Intervention non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    deja_existante = hasattr(intervention, 'facture')
    facture = services.creer_facture_pour_intervention(intervention)
    return Response(
        FactureSerializer(facture).data,
        status=status.HTTP_200_OK if deja_existante else status.HTTP_201_CREATED,
    )


def page_login(request):
    return render(request, 'login.html')


def page_register(request):
    return render(request, 'register.html')


def page_dashboard_client(request):
    return render(request, 'dashboard-client.html')


def page_dashboard_mecanicien(request):
    return render(request, 'dashboard-mecanicien.html')


def page_dashboard_admin(request):
    return render(request, 'dashboard-admin.html')
