from django import forms
from django.contrib.auth.forms import (AuthenticationForm,
                                       PasswordChangeForm,
                                       UserCreationForm)

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


class KanisaChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Change Password'
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))
        self.helper.form_class = 'form-horizontal'

        super(KanisaChangePasswordForm, self).__init__(*args, **kwargs)


class KanisaUserCreationForm(UserCreationForm):
    email = forms.EmailField(help_text=('We\'ll need an email address to get '
                                        'in touch with you to verify your '
                                        'account.'))

    fields = ('username', 'email', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Register'
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))

        super(KanisaUserCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(KanisaUserCreationForm, self).save(commit)
        user.is_active = False
        user.save()
        return user
