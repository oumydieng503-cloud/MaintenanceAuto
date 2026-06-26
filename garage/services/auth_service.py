from django.contrib.auth.models import User

from garage.models import Profil

ROLES_STAFF = {'mecanicien', 'administrateur'}


def _verifier_admin(admin_user):
    if not hasattr(admin_user, 'profil') or admin_user.profil.role != 'administrateur':
        raise PermissionError("Seul un administrateur peut effectuer cette action.")


def inscrire_client(username, password, email='', first_name='', last_name='', telephone='', adresse=''):
    if User.objects.filter(username=username).exists():
        raise ValueError("Ce nom d'utilisateur existe déjà.")

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    Profil.objects.create(
        user=user,
        role='client',
        telephone=telephone,
        adresse=adresse,
    )
    return user


def creer_utilisateur_staff(admin_user, username, password, email, first_name, last_name, role, telephone='', adresse=''):
    _verifier_admin(admin_user)

    if role not in ROLES_STAFF:
        raise ValueError("Seuls les rôles mécanicien et administrateur peuvent être créés par un admin.")

    if User.objects.filter(username=username).exists():
        raise ValueError("Ce nom d'utilisateur existe déjà.")

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    Profil.objects.create(
        user=user,
        role=role,
        telephone=telephone,
        adresse=adresse,
    )
    return user
