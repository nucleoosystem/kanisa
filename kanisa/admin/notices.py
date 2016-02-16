from django.contrib import admin
from kanisa.admin.base import KanisaBaseAdmin
from kanisa.models import SiteWideNotice


class SiteWideNoticeAdmin(KanisaBaseAdmin):
    list_display = ('headline',
                    'created',
                    'publish_until',
                    'published',
                    'expired', )

    search_fields = ('headline',
                     'contents', )

    list_filter = ('published', )

admin.site.register(SiteWideNotice, SiteWideNoticeAdmin)
