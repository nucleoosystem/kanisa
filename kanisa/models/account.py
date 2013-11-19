from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from sorl.thumbnail import ImageField


class RegisteredUser(AbstractUser):
    created = models.DateTimeField(null=True, blank=True, editable=False)
    updated = models.DateTimeField(null=True, blank=True, editable=False)
    image = ImageField(upload_to='kanisa/users', blank=True, null=True)

    class Meta:
        app_label = 'kanisa'
        ordering = ('last_name', 'first_name', )
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
