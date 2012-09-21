from django.contrib import admin
from kanisa.admin.base import KanisaBaseAdmin
from kanisa.models import (Document,
                           SermonSeries, SermonSpeaker, Sermon,
                           Page)
from mptt.admin import MPTTModelAdmin
from sorl.thumbnail import default
from sorl.thumbnail.admin import AdminImageMixin

import kanisa.admin.banners
import kanisa.admin.diary


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
