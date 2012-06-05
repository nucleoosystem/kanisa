from django.contrib import admin
from kanisa.conf import KANISA_ADMIN_THUMBS_SIZE
from kanisa.models.banners import Banner
from sorl.thumbnail import default
from sorl.thumbnail.admin import AdminImageMixin


class BannerAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = ('image_thumb', 'headline', 'url', 'publish_from', 'publish_until', 'active', )
    search_fields = ('headline', 'contents', 'url', )

    def image_thumb(self, obj):
        if obj.image:
            thumb = default.backend.get_thumbnail(obj.image.file,
                                                  KANISA_ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        else:
            return "No Image"
    image_thumb.short_description = 'Image'
    image_thumb.allow_tags = True

admin.site.register(Banner, BannerAdmin)
