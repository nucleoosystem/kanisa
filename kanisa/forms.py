from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from kanisa.models.banners import Banner
from kanisa.models.diary import DiaryEvent

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


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Save %s' % self._meta.model._meta.verbose_name.title()
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))
        self.helper.form_class = 'form-horizontal'

        super(BaseForm, self).__init__(*args, **kwargs)


class BannerForm(BaseForm):
    class Meta:
        model = Banner


class DiaryForm(BaseForm):
    start_time = BootstrapTimeField()

    class Meta:
        model = DiaryEvent
