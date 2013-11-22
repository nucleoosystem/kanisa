from django import forms
from kanisa.models import RegisteredUser
from kanisa.forms import KanisaBaseForm
from .widgets import KanisaThumbnailFileWidget


class UserUpdateForm(KanisaBaseForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    image = forms.FileField(widget=KanisaThumbnailFileWidget(100, 100))

    submit_text = 'Save Changes'
