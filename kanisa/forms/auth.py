from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class KanisaLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Login'
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))

        super(KanisaLoginForm, self).__init__(*args, **kwargs)
