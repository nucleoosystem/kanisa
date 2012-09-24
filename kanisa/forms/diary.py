from django import forms
from kanisa.forms import (KanisaBaseForm,
                          BootstrapTimeField,
                          BootstrapDateField)
from kanisa.models import EventContact, RegularEvent, ScheduledEvent


class EventContactForm(KanisaBaseForm):
    class Meta:
        model = EventContact


class RegularEventForm(KanisaBaseForm):
    start_time = BootstrapTimeField()

    class Meta:
        model = RegularEvent


class ScheduledEventEditForm(KanisaBaseForm):
    start_time = BootstrapTimeField()
    date = BootstrapDateField()

    class Meta:
        model = ScheduledEvent
        exclude = ('event', )


class ScheduledEventCreationForm(KanisaBaseForm):
    start_time = BootstrapTimeField()
    date = BootstrapDateField()
    event = forms.ModelChoiceField(queryset=RegularEvent.objects.
                                   order_by('title').all(),
                                   required=False)

    class Meta:
        model = ScheduledEvent

    class Media:
        js = ('kanisa/js/scheduled_event.js', )
