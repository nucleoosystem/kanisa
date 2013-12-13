from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from kanisa.conf import KANISA_ADMIN_THUMBS_SIZE
from kanisa.models import RegisteredUser
from sorl.thumbnail import default


class RegisteredUserAdmin(UserAdmin):
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

    def get_form(self, request, obj=None, **kwargs):
        form = super(RegisteredUserAdmin,
                     self).get_form(request, obj, **kwargs)

        form.base_fields['first_name'].required = True
        form.base_fields['last_name'].required = True
        form.base_fields['email'].required = True

        return form

    def image_thumb(self, obj):
        if obj.image:
            thumb = default.backend.get_thumbnail(obj.image.file,
                                                  KANISA_ADMIN_THUMBS_SIZE)
            return u'<img width="%s" height="%s" src="%s" />' % (thumb.width,
                                                                 thumb.height,
                                                                 thumb.url)
        return "No Image"
    image_thumb.short_description = 'Image'
    image_thumb.allow_tags = True

admin.site.register(RegisteredUser, RegisteredUserAdmin)
