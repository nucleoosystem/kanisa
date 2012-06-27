from django.contrib import admin
from kanisa.conf import KANISA_ADMIN_THUMBS_SIZE
from kanisa.models import (Banner,
                           RegularEvent, ScheduledEvent,
                           SermonSeries, SermonSpeaker, Sermon)
from sorl.thumbnail import default
from sorl.thumbnail.admin import AdminImageMixin


class BannerAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = ('image_thumb',
                    'headline',
                    'url',
                    'publish_from',
                    'publish_until',
                    'active', )

    search_fields = ('headline',
                     'contents',
                     'url', )

    def image_thumb(self, obj):
        if obj.image:
            thumb = default.backend.get_thumbnail(obj.image.file,
                                                  KANISA_ADMIN_THUMBS_SIZE)
            return u'<img width="%s" height="%s" src="%s" />' % (thumb.width,
                                                                 thumb.height,
                                                                 thumb.url)
        else:
            return "No Image"
    image_thumb.short_description = 'Image'
    image_thumb.allow_tags = True

admin.site.register(Banner, BannerAdmin)


class RegularEventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'day', 'start_time', )
    list_filter = ('day', )

admin.site.register(RegularEvent, RegularEventAdmin)


class ScheduledEventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'event', 'date', )

admin.site.register(ScheduledEvent, ScheduledEventAdmin)


class SermonSeriesAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'passage', )

admin.site.register(SermonSeries, SermonSeriesAdmin)


class SermonSpeakerAdmin(admin.ModelAdmin):
    search_fields = ('forename', 'surname', )
    list_display = ('forename', 'surname', )

admin.site.register(SermonSpeaker, SermonSpeakerAdmin)


class SermonAdmin(admin.ModelAdmin):
    search_fields = ('title', 'details', )
    list_display = ('title', 'date', 'passage', 'series', 'speaker', )

admin.site.register(Sermon, SermonAdmin)
