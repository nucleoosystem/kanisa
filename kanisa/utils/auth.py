from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Q


def has_any_kanisa_permission(user):
    perms = user.get_all_permissions()
    kanisa_management = [p for p in perms if p.startswith('kanisa.manage')]
    return len(kanisa_management) > 0


def users_with_perm(perm):
    permission = Permission.objects.get(codename=perm)
    cond = Q(groups__permissions=permission) | Q(user_permissions=permission)
    unique_users = get_user_model().objects.filter(cond).distinct()
    return unique_users.filter(is_active=True)
