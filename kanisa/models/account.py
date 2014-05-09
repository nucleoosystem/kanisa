from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.timezone import now
from kanisa.utils.branding import BrandingInformation
from sorl.thumbnail import ImageField


class RegisteredUser(AbstractUser):
    created = models.DateTimeField(null=True, blank=True, editable=False)
    updated = models.DateTimeField(null=True, blank=True, editable=False)
    image = ImageField(upload_to='kanisa/users', blank=True, null=True)

    class Meta:
        app_label = 'kanisa'
        ordering = ('last_name', 'first_name', )
        permissions = (
            ('manage_users',
             'Can manage your users'),
        )
        verbose_name = 'registered user'
        verbose_name_plural = 'registered users'

    def save(self, **kwargs):
        if not self.pk:
            self.created = now()

        self.updated = now()
        super(RegisteredUser, self).save(**kwargs)

    def get_familiar_name(self):
        if self.first_name:
            return self.first_name

        return self.username

    def get_display_name(self):
        full = self.get_full_name()

        if full:
            return full

        return self.username

    def get_kanisa_permissions(self):
        permissions = self.user_permissions.filter(
            content_type__app_label='kanisa'
        )

        return permissions

    def set_kanisa_permissions(self, perms):
        # Clear existing permissions
        existing_permissions = self.get_kanisa_permissions()
        for p in existing_permissions:
            self.user_permissions.remove(p)

        # Add the ones we asked for
        all_perms = Permission.objects.filter(content_type__app_label='kanisa')
        for p in all_perms:
            if p.codename in perms:
                self.user_permissions.add(p)

    def can_see_service_plans(self):
        if hasattr(self, '_can_see_service_plans'):
            return self._can_see_service_plans

        self._can_see_service_plans = False

        # Does the user have permission to manage services?
        if self.has_perm('kanisa.manage_services'):
            self._can_see_service_plans = True
        # Is the user the band leader of any bands?
        elif self.band_set.count() > 0:
            self._can_see_service_plans = True
        # Is the user a band member in any bands?
        elif self.band_musicians.count() > 0:
            self._can_see_service_plans = True
        # Is the user leading the band in any services?
        elif self.service_set.count() > 0:
            self._can_see_service_plans = True
        # Is the user playing in any services?
        elif self.service_musicians.count() > 0:
            self._can_see_service_plans = True

        return self._can_see_service_plans

    def image_or_default(self):
        if self.image:
            return self.image

        branding = BrandingInformation('apple')
        return branding.url
