from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profils', views.ProfilViewSet, basename='profil')
router.register(r'vehicules', views.VehiculeViewSet, basename='vehicule')
router.register(r'rendezvous', views.RendezVousViewSet, basename='rendezvous')
router.register(r'interventions', views.InterventionViewSet, basename='intervention')
router.register(r'pieces', views.PieceViewSet)
router.register(r'factures', views.FactureViewSet, basename='facture')

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.register, name='register'),
    path('auth/creer-staff/', views.creer_staff, name='creer-staff'),
    path('profils/me/', views.profil_me, name='profil-me'),
    path('', include(router.urls)),
    path(
        'interventions/<int:intervention_id>/ajouter-piece/',
        views.ajouter_piece_intervention,
        name='ajouter-piece',
    ),
    path(
        'interventions/<int:intervention_id>/generer-facture/',
        views.generer_facture,
        name='generer-facture',
    ),
    path(
        'factures/<int:facture_id>/recalculer/',
        views.recalculer_facture_view,
        name='recalculer-facture',
    ),
]
