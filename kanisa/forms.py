from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from kanisa.models import (Banner,
                           RegularEvent, ScheduledEvent,
                           Document,
                           SermonSeries, Sermon)


TIMEPICKER_FORMAT = '%I:%M %p'


class BootstrapTimeWidget(forms.widgets.TimeInput):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = TIMEPICKER_FORMAT
        extra_attrs = {'data-provide': 'timepicker', 'class': 'timepicker'}

        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}

        kwargs['attrs'].update(extra_attrs)

        super(BootstrapTimeWidget, self).__init__(*args, **kwargs)

    class Media:
        css = {'all': ['kanisa/bootstrap/css/timepicker.css', ]}
        js = ('kanisa/bootstrap/js/bootstrap-timepicker.js', )


class BootstrapTimeField(forms.TimeField):
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = [TIMEPICKER_FORMAT, ]
        kwargs['widget'] = BootstrapTimeWidget
        super(BootstrapTimeField, self).__init__(*args, **kwargs)


class BootstrapDateWidget(forms.widgets.DateInput):
    def __init__(self, *args, **kwargs):
        extra_attrs = {'data-date-format': 'dd/mm/yyyy', 'class': 'datepicker'}

        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}

        kwargs['attrs'].update(extra_attrs)

        super(BootstrapDateWidget, self).__init__(*args, **kwargs)

    class Media:
        css = {'all': ['kanisa/bootstrap/css/datepicker.css', ]}
        js = ('kanisa/bootstrap/js/bootstrap-datepicker.js', )


class BootstrapDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = BootstrapDateWidget
        super(BootstrapDateField, self).__init__(*args, **kwargs)


class KanisaBaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Save %s' % self._meta.model._meta.verbose_name.title()
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))
        self.helper.form_class = 'form-horizontal'

        super(KanisaBaseForm, self).__init__(*args, **kwargs)


class BannerForm(KanisaBaseForm):
    publish_from = BootstrapDateField(required=False)
    publish_until = BootstrapDateField(required=False)

    class Meta:
        model = Banner


class RegularEventForm(KanisaBaseForm):
    start_time = BootstrapTimeField()

    class Meta:
        model = RegularEvent


class ScheduledEventEditForm(KanisaBaseForm):
    start_time = BootstrapTimeField()

    class Meta:
        model = ScheduledEvent
        exclude = ('event', 'date', )

    def clean(self):
        cleaned_data = self.cleaned_data

        if not self.instance.pk:
            return cleaned_data

        title = cleaned_data['title']

        if not title and not self.instance.event:
            msg = 'Your event must have a title.'
            self._errors["title"] = self.error_class([msg])
            del cleaned_data["title"]

        return cleaned_data


class ScheduledEventCreationForm(KanisaBaseForm):
    start_time = BootstrapTimeField()
    date = BootstrapDateField()

    class Meta:
        model = ScheduledEvent


class SermonSeriesForm(KanisaBaseForm):
    class Meta:
        model = SermonSeries


class SermonForm(KanisaBaseForm):
    date = BootstrapDateField()

    class Meta:
        model = Sermon


class DocumentForm(KanisaBaseForm):
    class Meta:
        model = Document
