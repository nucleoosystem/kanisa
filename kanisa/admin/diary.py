from django.contrib import admin
from kanisa.models import (
    RegularEvent,
    ScheduledEvent,
    ScheduledEventSeries,
    EventCategory
)


class RegularEventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'intro', 'details', )
    list_display = (
        'title',
        'pattern_description',
        'autoschedule',
        'mothballed',
    )
    list_filter = (
        'autoschedule',
        'mothballed',
    )

admin.site.register(RegularEvent, RegularEventAdmin)


class ScheduledEventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'event', 'date', )

admin.site.register(ScheduledEvent, ScheduledEventAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', )

admin.site.register(EventCategory, EventCategoryAdmin)


class ScheduledEventSeriesAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', )

admin.site.register(ScheduledEventSeries, ScheduledEventSeriesAdmin)
