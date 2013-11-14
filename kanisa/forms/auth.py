from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (AuthenticationForm,
                                       PasswordChangeForm,
                                       UserCreationForm)
from kanisa.forms import (
    KanisaBaseModelForm,
    KanisaPrettyForm
)
from password_reset.forms import PasswordRecoveryForm, PasswordResetForm


class KanisaLoginForm(KanisaPrettyForm, AuthenticationForm):
    submit_text = 'Login'

    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaLoginForm, self).__init__(*args, **kwargs)


class KanisaChangePasswordForm(KanisaPrettyForm, PasswordChangeForm):
    submit_text = 'Change Password'

    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaChangePasswordForm, self).__init__(*args, **kwargs)


class KanisaUserCreationForm(KanisaPrettyForm, UserCreationForm):
    submit_text = 'Register'

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(help_text=('We\'ll need an email address to get '
                                        'in touch with you to verify your '
                                        'account.'))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )

    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaUserCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(KanisaUserCreationForm, self).save(commit)
        user.is_active = False
        user.save()
        return user


class KanisaPasswordRecoveryForm(KanisaPrettyForm, PasswordRecoveryForm):
    submit_text = 'Recover my password'

    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaPasswordRecoveryForm, self).__init__(*args, **kwargs)


class KanisaPasswordResetForm(KanisaPrettyForm, PasswordResetForm):
    submit_text = 'Reset my password'

    def __init__(self, *args, **kwargs):
        self.helper = self.get_form_helper()
        super(KanisaPasswordResetForm, self).__init__(*args, **kwargs)


class KanisaAccountModificationForm(KanisaBaseModelForm):
    submit_text = 'Save Changes'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]
