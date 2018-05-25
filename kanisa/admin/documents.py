from django.contrib import admin
from kanisa.models import Document


class DocumentAdmin(admin.ModelAdmin):
    search_fields = (
        'title',
        'details',
    )
    list_display = (
        'title',
        'modified',
        'downloads',
        'expiry_months',
        'has_expired',
    )
    date_hierarchy = 'created'
    list_filter = (
        'expiry_months',
        'expired',
    )

admin.site.register(Document, DocumentAdmin)
