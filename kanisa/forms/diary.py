from django import forms
from kanisa.forms import (KanisaBaseForm,
                          BootstrapTimeField,
                          BootstrapDateField)
from kanisa.forms.widgets import KanisaMainInputWidget
from kanisa.models import EventContact, RegularEvent, ScheduledEvent


class EventContactForm(KanisaBaseForm):
    class Meta:
        model = EventContact


class RegularEventForm(KanisaBaseForm):
    start_time = BootstrapTimeField()

    class Meta:
        model = RegularEvent
        widgets = {'details': KanisaMainInputWidget(), }


class ScheduledEventEditForm(KanisaBaseForm):
    start_time = BootstrapTimeField()
    date = BootstrapDateField()

    class Meta:
        model = ScheduledEvent
        exclude = ('event', )
        widgets = {'details': KanisaMainInputWidget(), }


class ScheduledEventCreationForm(KanisaBaseForm):
    start_time = BootstrapTimeField()
    date = BootstrapDateField()
    event = forms.ModelChoiceField(queryset=RegularEvent.objects.
                                   order_by('title').all(),
                                   required=False)

    class Meta:
        model = ScheduledEvent
        widgets = {'details': KanisaMainInputWidget(), }

    class Media:
        js = ('kanisa/js/scheduled_event.js', )
