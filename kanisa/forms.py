from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from kanisa.models.banners import Banner


class BannerForm(ModelForm):
    class Meta:
        model = Banner

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        self.helper.add_input(Submit('submit', 'Save Banner',
                                     css_class=css))
        self.helper.form_class = 'form-horizontal'

        super(BannerForm, self).__init__(*args, **kwargs)
