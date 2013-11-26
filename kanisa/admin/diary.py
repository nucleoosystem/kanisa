from django.contrib import admin
from kanisa.admin.base import KanisaBaseAdmin
from kanisa.models import (
    EventContact,
    RegularEvent,
    ScheduledEvent,
    EventCategory
)
from sorl.thumbnail.admin import AdminImageMixin


class EventContactAdmin(KanisaBaseAdmin, AdminImageMixin):
    search_fields = ('name', 'email', )
    list_display = ('image_thumb',
                    'name', )

admin.site.register(EventContact, EventContactAdmin)


class RegularEventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title',
                    'pattern_description',
                    'start_time',
                    'autoschedule', )
    list_filter = ('autoschedule', )

admin.site.register(RegularEvent, RegularEventAdmin)


class ScheduledEventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'event', 'date', )

admin.site.register(ScheduledEvent, ScheduledEventAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', )

admin.site.register(EventCategory, EventCategoryAdmin)
