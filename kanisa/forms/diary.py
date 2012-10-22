from django import forms
from kanisa.forms import (KanisaBaseForm,
                          BootstrapTimeField,
                          BootstrapDateField)
from kanisa.forms.widgets import (KanisaMainInputWidget,
                                  KanisaTinyInputWidget)
from kanisa.models import EventContact, RegularEvent, ScheduledEvent


class EventContactForm(KanisaBaseForm):
    class Meta:
        model = EventContact


class RegularEventForm(KanisaBaseForm):
    start_time = BootstrapTimeField()

    class Meta:
        model = RegularEvent
        widgets = {'intro': KanisaTinyInputWidget(),
                   'details': KanisaMainInputWidget(), }


class ScheduledEventBaseForm(KanisaBaseForm):
    start_time = BootstrapTimeField()
    date = BootstrapDateField()
    end_date = BootstrapDateField(required=False)
    is_multi_day = forms.BooleanField(label='Multi-day event',
                                      required=False,
                                      help_text=('Check this box if this '
                                                 'event spans multiple '
                                                 'days.'))

    def __init__(self, *args, **kwargs):
        super(ScheduledEventBaseForm, self).__init__(*args, **kwargs)

        index_of_date = [i for i, x in enumerate(self.fields.keyOrder)
                         if x == 'start_time'][0]
        self.fields.keyOrder.pop()
        self.fields.keyOrder.insert(index_of_date + 1, 'is_multi_day')

    class Media:
        js = ('kanisa/js/scheduled_event.js', )


class ScheduledEventEditForm(ScheduledEventBaseForm):
    class Meta:
        model = ScheduledEvent
        exclude = ('event', )
        widgets = {'details': KanisaMainInputWidget(), }


class ScheduledEventCreationForm(ScheduledEventBaseForm):
    event = forms.ModelChoiceField(queryset=RegularEvent.objects.
                                   order_by('title').all(),
                                   required=False)

    class Meta:
        model = ScheduledEvent
        widgets = {'details': KanisaMainInputWidget(), }
