from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .widgets import (
    BootstrapDateWidget,
    BootstrapTimeWidget,
    TIMEPICKER_FORMAT
)


class BootstrapTimeField(forms.TimeField):
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = [TIMEPICKER_FORMAT, ]
        kwargs['widget'] = BootstrapTimeWidget
        super(BootstrapTimeField, self).__init__(*args, **kwargs)


class BootstrapDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = BootstrapDateWidget
        super(BootstrapDateField, self).__init__(*args, **kwargs)


class KanisaPrettyForm(object):
    def get_form_helper(self):
        helper = FormHelper()
        helper.label_class = 'col-lg-2'
        helper.field_class = 'col-lg-10'

        helper.add_input(Submit('submit',
                                self.get_submit_text(),
                                css_class=self.get_submit_css()))
        helper.form_class = 'form-horizontal'

        if hasattr(self, 'kanisa_form_class'):
            klass = self.kanisa_form_class
        else:
            klass = self.__class__.__name__.lower()

        helper.form_class += ' ' + klass

        return helper

    def get_submit_css(self):
        return "btn-primary btn-lg btn-success"

    def get_submit_text(self):
        if hasattr(self, 'submit_text'):
            return self.submit_text

        raise ImproperlyConfigured("Pretty forms must have submit_text "
                                   "defined.")


class KanisaBaseModelForm(KanisaPrettyForm, ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaBaseModelForm, self).__init__(*args, **kwargs)

    def add_save_and_continue(self):
        self.helper.add_input(
            Submit(
                "continue",
                "Save & Continue Editing",
                css_class="btn-lg btn-primary"
            )
        )

    def get_submit_text(self):
        if hasattr(self, 'submit_text'):
            return self.submit_text

        return 'Save %s' % self._meta.model._meta.verbose_name.title()


class KanisaBaseForm(KanisaPrettyForm, forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaBaseForm, self).__init__(*args, **kwargs)
