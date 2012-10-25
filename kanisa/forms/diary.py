from django import forms
from django.forms.util import ErrorList
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

    def clean(self):
        super(ScheduledEventBaseForm, self).clean()
        cleaned_data = self.cleaned_data

        if cleaned_data['end_date'] and cleaned_data['date']:
            if cleaned_data['end_date'] < cleaned_data['date']:
                errors = ErrorList(['The event cannot end before it starts.'])
                self._errors["end_date"] = errors
                del cleaned_data["end_date"]

        return cleaned_data


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
