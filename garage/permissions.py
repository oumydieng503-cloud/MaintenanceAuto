from rest_framework import permissions


class EstAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'profil') and request.user.profil.role == 'administrateur'


class EstMecanicien(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'profil') and request.user.profil.role == 'mecanicien'


class EstClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'profil') and request.user.profil.role == 'client'


class EstAdminOuMecanicien(permissions.BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'profil'):
            return False
        return request.user.profil.role in ('administrateur', 'mecanicien')
