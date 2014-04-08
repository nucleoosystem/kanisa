from datetime import date, timedelta
from django.db.models import Count
from kanisa.models import Song


def most_popular_songs(cutoff=None, service_filter=None):
    if cutoff is None:
        cutoff = date.today() - timedelta(days=365)

    songs = Song.objects.all()
    songs = songs.filter(songinservice__service__event__date__gte=cutoff)

    if service_filter:
        songs = songs.filter(
            songinservice__service__event__event=service_filter
        )

    songs = songs.annotate(usage=Count('songinservice'))
    songs = songs.order_by('-usage')
    return songs
