from django.contrib.auth.models import Permission, User
from django.db.models import Q


def has_any_kanisa_permission(user):
    perms = user.get_all_permissions()
    kanisa_management = [p for p in perms if p.startswith('kanisa.manage')]
    return len(kanisa_management) > 0


def users_with_perm(perm):
    permission = Permission.objects.get(codename=perm)
    cond = Q(groups__permissions=permission) | Q(user_permissions=permission)
    return User.objects.filter(cond).distinct().filter(is_active=True)
