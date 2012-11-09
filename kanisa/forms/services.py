from django import forms
from kanisa.forms import KanisaBaseForm, KanisaBaseModelForm
from kanisa.models import Song, Service


class AddSongToServiceForm(KanisaBaseForm):
    song = forms.ModelChoiceField(queryset=Song.objects.all())
    submit_text = 'Add Song'


class ServiceForm(KanisaBaseModelForm):
    class Meta:
        model = Service
        exclude = ('songs', )
