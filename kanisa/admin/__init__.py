from django.contrib import admin
from kanisa.admin.base import KanisaBaseAdmin
from kanisa.models import (Banner,
                           EventContact, RegularEvent, ScheduledEvent,
                           Document,
                           SermonSeries, SermonSpeaker, Sermon,
                           Page)
from mptt.admin import MPTTModelAdmin
from sorl.thumbnail import default
from sorl.thumbnail.admin import AdminImageMixin


class BannerAdmin(KanisaBaseAdmin, AdminImageMixin):
    list_display = ('image_thumb',
                    'headline',
                    'url',
                    'publish_from',
                    'publish_until',
                    'active', )

    search_fields = ('headline',
                     'contents',
                     'url', )

admin.site.register(Banner, BannerAdmin)


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


class DocumentAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'modified', )

admin.site.register(Document, DocumentAdmin)


class SermonSeriesAdmin(KanisaBaseAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'image_thumb', 'passage', )

admin.site.register(SermonSeries, SermonSeriesAdmin)


class SermonSpeakerAdmin(KanisaBaseAdmin):
    search_fields = ('forename', 'surname', )
    list_display = ('name', 'image_thumb', )

admin.site.register(SermonSpeaker, SermonSpeakerAdmin)


class SermonAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'date', 'passage', 'series', 'speaker', )

admin.site.register(Sermon, SermonAdmin)


class PageAdmin(MPTTModelAdmin):
    pass

admin.site.register(Page, PageAdmin)
