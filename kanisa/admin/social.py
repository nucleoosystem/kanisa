from django.contrib import admin
from kanisa.models import ScheduledTweet


class ScheduledTweetAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'date', 'time', 'posted', )
    list_filter = ('posted', )
    date_hierarchy = 'date'

admin.site.register(ScheduledTweet, ScheduledTweetAdmin)
