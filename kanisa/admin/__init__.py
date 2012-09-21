from django.contrib import admin
from kanisa.admin.base import KanisaBaseAdmin
from kanisa.models import Page
from mptt.admin import MPTTModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

import kanisa.admin.banners
import kanisa.admin.diary
import kanisa.admin.documents
import kanisa.admin.sermons


class PageAdmin(MPTTModelAdmin):
    pass

admin.site.register(Page, PageAdmin)
