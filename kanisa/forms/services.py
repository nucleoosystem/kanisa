from django import forms
from django.contrib.auth.models import User
from django.utils import formats
from crispy_forms.layout import Layout, HTML
from kanisa.forms import KanisaBaseForm, KanisaBaseModelForm
from kanisa.models import Song, Service, ScheduledEvent


class AddSongToServiceForm(KanisaBaseForm):
    song = forms.ModelChoiceField(queryset=Song.objects.all())
    submit_text = 'Add Song'


class CreateSongForm(KanisaBaseModelForm):
    submit_text = 'Create Song'

    def get_form_helper(self):
        helper = super(CreateSongForm, self).get_form_helper()
        helper.layout = Layout(
            'title',
            'composers',
            HTML('{% include "kanisa/members/services/_composer_add.html" %}'),
            )
        return helper

    class Meta:
        model = Song


class EventChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        event_date = formats.date_format(obj.date, "DATE_FORMAT")
        return '%s (%s)' % (unicode(obj), event_date)


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = obj.get_full_name()
        return full_name or obj.username


class ServiceForm(KanisaBaseModelForm):
    event = EventChoiceField(ScheduledEvent.objects.all())
    band_leader = UserChoiceField(User.objects.all())

    class Meta:
        model = Service
        exclude = ('songs', )
