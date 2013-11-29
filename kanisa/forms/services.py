from django import forms
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import formats
from crispy_forms.layout import Layout, HTML
from kanisa.forms import KanisaBaseForm, KanisaBaseModelForm
from kanisa.models import (
    Song,
    Service,
    ScheduledEvent,
    Composer,
    Band
)


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

    class Media:
        js = ('kanisa/js/services_add_song.js', )


class EventChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        event_date = formats.date_format(obj.date, "DATE_FORMAT")
        return '%s (%s)' % (unicode(obj), event_date)


class AccountChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = obj.get_full_name()
        return full_name or obj.username


class MultipleAccountChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        full_name = obj.get_full_name()
        return full_name or obj.username


class ServiceForm(KanisaBaseModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            del self.fields['band']
        else:
            url = reverse('kanisa_xhr_bandinformation')
            self.helper.attrs["data-band-info-url"] = url

    event = EventChoiceField(ScheduledEvent.objects.all())
    band = forms.ModelChoiceField(Band.objects.all(), required=False)
    band_leader = AccountChoiceField(get_user_model().objects.all())
    musicians = MultipleAccountChoiceField(
        get_user_model().objects.all(),
        required=False
    )

    class Media:
        js = ('kanisa/js/services.js', )

    class Meta:
        fields = ('event', 'band', 'band_leader', 'musicians', )
        model = Service


class ComposerForm(KanisaBaseModelForm):
    class Meta:
        model = Composer
