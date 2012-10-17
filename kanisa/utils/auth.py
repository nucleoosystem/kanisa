def has_any_kanisa_permission(user):
    perms = user.get_all_permissions()
    kanisa_management = [p for p in perms if p.startswith('kanisa.manage')]
    return len(kanisa_management) > 0
