from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from kanisa.models.banners import Banner
from kanisa.models.diary import DiaryEvent


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
    class Meta:
        model = DiaryEvent
