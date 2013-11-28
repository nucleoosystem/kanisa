from django.core.management.base import BaseCommand
from kanisa.models import RegularEvent


class Command(BaseCommand):
    help = ('Guesses event schedule for each regular event based on existing '
            'events')

    def handle(self, *args, **options):
        for event in RegularEvent.objects.all():
            self.handle_event(event)

    def get_single_most_common(self, values):
        threshold = len(values) / 3
        counts = [(d, values.count(d)) for d in set(values)]
        common = [d for (d, count) in counts
                  if count > threshold]

        if len(common) == 1:
            return common[0]

        return None

    def handle_event(self, event):
        matching_events = event.scheduledevent_set.all()

        most_common_duration = self.get_single_most_common(
            [e.duration for e in matching_events]
        )

        most_common_start_time = self.get_single_most_common(
            [e.start_time for e in matching_events]
        )

        if most_common_duration:
            print "Setting duration of %s to %d minutes." % (
                event,
                most_common_duration
            )
            event.duration = most_common_duration

        if most_common_start_time:
            print "Setting start time of %s to %s." % (
                event,
                most_common_start_time.strftime("%H:%M")
            )
            event.start_time = most_common_start_time

        event.save()
