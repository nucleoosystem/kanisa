from django.contrib import admin
from kanisa.admin.base import KanisaBaseAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from kanisa.models import RegisteredUser


class RegisteredUserAdmin(KanisaBaseAdmin, UserAdmin):
    list_display = (
        'username',
        'image_thumb',
        'first_name',
        'last_name',
        'created',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(RegisteredUser, RegisteredUserAdmin)