from django import forms
from kanisa.forms import (KanisaBaseForm,
                          BootstrapTimeField,
                          BootstrapDateField,
                          EpicWidget)
from kanisa.models import RegularEvent, ScheduledEvent


class RegularEventForm(KanisaBaseForm):
    start_time = BootstrapTimeField()

    class Meta:
        model = RegularEvent
        widgets = {'details': EpicWidget(), }


class ScheduledEventEditForm(KanisaBaseForm):
    start_time = BootstrapTimeField()
    date = BootstrapDateField()

    class Meta:
        model = ScheduledEvent
        exclude = ('event', )
        widgets = {'details': EpicWidget(), }


class ScheduledEventCreationForm(KanisaBaseForm):
    start_time = BootstrapTimeField()
    date = BootstrapDateField()
    event = forms.ModelChoiceField(queryset=RegularEvent.objects.
                                   order_by('title').all(),
                                   required=False)

    class Meta:
        model = ScheduledEvent
        widgets = {'details': EpicWidget(), }

    class Media:
        js = ('kanisa/js/scheduled_event.js', )
