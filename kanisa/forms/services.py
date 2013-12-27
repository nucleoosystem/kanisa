from django import forms
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from crispy_forms.layout import Layout, HTML
from kanisa.forms import (
    BootstrapDateField,
    KanisaBaseForm,
    KanisaBaseModelForm
)
from kanisa.forms.utils import KanisaMediaWidget
from kanisa.models import (
    Song,
    Service,
    ScheduledEvent,
    Composer,
    Band
)
from kanisa.forms.widgets import KanisaAccountMultipleSelector


class AddSongToServiceForm(KanisaBaseForm):
    song = forms.ModelChoiceField(queryset=Song.objects.all())
    submit_text = 'Add Song'


class CreateSongForm(KanisaBaseModelForm, KanisaMediaWidget):
    submit_text = 'Create Song'

    def get_form_helper(self):
        helper = super(CreateSongForm, self).get_form_helper()
        helper.layout = Layout(
            'title',
            'composers',
            HTML('{% include '
                 '"kanisa/management/services/_composer_add.html" '
                 '%}'),
        )
        return helper

    class Meta:
        model = Song

    class KanisaMedia:
        js = ('kanisa/js/kanisa_songs.js', )


class EventChoiceField(forms.ModelChoiceField):
    # This is only used when the field is hidden, and is designed to
    # make the view a bit faster to render.
    def label_from_instance(self, obj):
        return obj.pk


class AccountChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = obj.get_full_name()
        return full_name or obj.username


class MultipleAccountChoiceField(forms.ModelMultipleChoiceField):
    widget = KanisaAccountMultipleSelector

    def label_from_instance(self, obj):
        full_name = obj.get_full_name()
        return full_name or obj.username


class ServiceForm(KanisaBaseModelForm, KanisaMediaWidget):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            del self.fields['event']
            del self.fields['date']
            del self.fields['band']
        else:
            url = reverse('kanisa_xhr_bandinformation')
            self.helper.attrs["data-band-info-url"] = url
            url = reverse('kanisa_xhr_eventinformation')
            self.helper.attrs["data-event-info-url"] = url

    date = BootstrapDateField()
    # The list of events in the field events is largely ignored. We
    # need to specify .all() to ensure that any event which is
    # selected (after the user has selected a date) is accepted. With
    # ScheduledEvent.objects.none(), the view renders more quickly,
    # but no events are accepted when the user hits submit.
    event = EventChoiceField(ScheduledEvent.bare_objects.all())
    band = forms.ModelChoiceField(Band.objects.all(), required=False)
    band_leader = AccountChoiceField(get_user_model().objects.all())
    musicians = MultipleAccountChoiceField(
        get_user_model().objects.all(),
        required=False
    )

    class KanisaMedia:
        js = ('kanisa/js/services.js', )

    class Meta:
        fields = ('date', 'event', 'band', 'band_leader', 'musicians', )
        model = Service


class ComposerForm(KanisaBaseModelForm):
    class Meta:
        model = Composer


class BandForm(KanisaBaseModelForm):
    band_leader = AccountChoiceField(get_user_model().objects.all())
    musicians = MultipleAccountChoiceField(
        get_user_model().objects.all(),
        required=False
    )

    class Meta:
        model = Band
