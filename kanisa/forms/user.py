from crispy_forms.layout import (
    Fieldset,
    Layout
)
from django import forms
from django.contrib.auth.models import Permission
from kanisa.forms import KanisaBaseForm
from .widgets import (
    KanisaInlineCheckboxes,
    KanisaThumbnailFileWidget
)


def get_choices():
    all_perms = Permission.objects.filter(content_type__app_label='kanisa')
    return [(p.codename, p.name) for p in all_perms
            if p.codename.startswith('manage')]


class UserUpdateForm(KanisaBaseForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    image = forms.FileField(widget=KanisaThumbnailFileWidget(100, 100))
    permissions = forms.MultipleChoiceField(choices=get_choices(),
                                            label='',
                                            required=False)

    submit_text = 'Save Changes'

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                'Profile',
                'first_name',
                'last_name',
                'email',
                'image',
            ),
            Fieldset(
                'Permissions',
                KanisaInlineCheckboxes('permissions'),
            ),
        )
