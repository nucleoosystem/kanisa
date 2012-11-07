from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


TIMEPICKER_FORMAT = '%I:%M %p'


class BootstrapTimeWidget(forms.widgets.TimeInput):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = TIMEPICKER_FORMAT
        extra_attrs = {'data-provide': 'timepicker',
                       'class': 'timepicker'}

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
        extra_attrs = {'data-date-format': 'dd/mm/yyyy',
                       'class': 'datepicker'}

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


class KanisaPrettyForm(object):
    def get_form_helper(self):
        helper = FormHelper()

        helper.add_input(Submit('submit',
                                self.get_submit_text(),
                                css_class=self.get_submit_css()))
        helper.form_class = 'form-horizontal'
        return helper

    def get_submit_css(self):
        return "btn-primary btn-large btn-success"

    def get_submit_text(self):
        if hasattr(self, 'submit_text'):
            return self.submit_text

        raise ImproperlyConfigured("Pretty forms must have submit_text "
                                   "defined.")


class KanisaBaseForm(KanisaPrettyForm, ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaBaseForm, self).__init__(*args, **kwargs)

    def get_submit_text(self):
        return 'Save %s' % self._meta.model._meta.verbose_name.title()


class KanisaBaseModellessForm(KanisaPrettyForm, forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaBaseModellessForm, self).__init__(*args, **kwargs)
