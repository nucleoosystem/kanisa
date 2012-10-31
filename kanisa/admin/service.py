from django.contrib import admin
from kanisa.admin.base import KanisaBaseAdmin
from kanisa.models import (Composer,
                           Song,
                           Service,
                           SongInService)


class ComposerAdmin(KanisaBaseAdmin):
    search_fields = ('forename', 'surname', )
    list_display = ('full_name_reversed', )

admin.site.register(Composer, ComposerAdmin)


class SongAdmin(KanisaBaseAdmin):
    search_fields = ('title', )
    list_display = ('title', )

admin.site.register(Song, SongAdmin)


class SongInline(admin.TabularInline):
    model = SongInService


class ServiceAdmin(KanisaBaseAdmin):
    inlines = [
        SongInline,
    ]

admin.site.register(Service, ServiceAdmin)
