from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from kanisa.models.banners import Banner


class BannerCreationForm(ModelForm):
    class Meta:
        model = Banner

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        self.helper.add_input(Submit('submit', 'Create Banner',
                                     css_class=css))
        super(BannerCreationForm, self).__init__(*args, **kwargs)
