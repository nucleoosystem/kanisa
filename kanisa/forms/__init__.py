from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.forms.util import ErrorList

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datetime import datetime
from kanisa import conf
from kanisa.widgets import EpicWidget
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from kanisa.models import (Banner,
                           Document,
                           SermonSeries, Sermon, SermonSpeaker,
                           ScheduledTweet,
                           Page)


TIMEPICKER_FORMAT = '%I:%M %p'


class BootstrapTimeWidget(forms.widgets.TimeInput):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = TIMEPICKER_FORMAT
        extra_attrs = {'data-provide': 'timepicker', 'class': 'timepicker'}

        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}

        kwargs['attrs'].update(extra_attrs)

        super(BootstrapTimeWidget, self).__init__(*args, **kwargs)

    class Media:
        css = {'all': ['kanisa/bootstrap/css/timepicker.css', ]}
        js = ('kanisa/bootstrap/js/bootstrap-timepicker.js', )


class BootstrapTimeField(forms.TimeField):
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = [TIMEPICKER_FORMAT, ]
        kwargs['widget'] = BootstrapTimeWidget
        super(BootstrapTimeField, self).__init__(*args, **kwargs)


class BootstrapDateWidget(forms.widgets.DateInput):
    def __init__(self, *args, **kwargs):
        extra_attrs = {'data-date-format': 'dd/mm/yyyy', 'class': 'datepicker'}

        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}

        kwargs['attrs'].update(extra_attrs)

        super(BootstrapDateWidget, self).__init__(*args, **kwargs)

    class Media:
        css = {'all': ['kanisa/bootstrap/css/datepicker.css', ]}
        js = ('kanisa/bootstrap/js/bootstrap-datepicker.js', )


class BootstrapDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = BootstrapDateWidget
        super(BootstrapDateField, self).__init__(*args, **kwargs)


class KanisaBaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Save %s' % self._meta.model._meta.verbose_name.title()
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))
        self.helper.form_class = 'form-horizontal'

        super(KanisaBaseForm, self).__init__(*args, **kwargs)


class BannerForm(KanisaBaseForm):
    publish_from = BootstrapDateField(required=False,
                                      help_text=('The date at which your '
                                                 'banner will become visible '
                                                 'on the website. If left '
                                                 'blank the start date is '
                                                 'unrestricted.'))
    publish_until = BootstrapDateField(required=False,
                                       help_text=('The final date on which '
                                                  'your banner will be '
                                                  'visible. If left blank '
                                                  'your banner will be '
                                                  'visible indefinitely.'))

    class Meta:
        exclude = ('visits', )
        model = Banner


class SermonSeriesForm(KanisaBaseForm):
    class Meta:
        model = SermonSeries
        widgets = {'details': EpicWidget(), }


class SermonSpeakerForm(KanisaBaseForm):
    class Meta:
        model = SermonSpeaker


class SermonForm(KanisaBaseForm):
    date = BootstrapDateField()

    class Meta:
        model = Sermon
        widgets = {'details': EpicWidget(), }

    def clean(self):
        super(SermonForm, self).clean()
        cleaned_data = self.cleaned_data

        if u'mp3' in self.files:
            if hasattr(self.files['mp3'], 'temporary_file_path'):
                audio = MP3(self.files['mp3'].temporary_file_path())
            else:
                # You probably need to set FILE_UPLOAD_HANDLERS to
                # django.core.files.uploadhandler.TemporaryFileUploadHandler
                audio = None

            if not audio or not audio.info or audio.info.sketchy:
                errors = ErrorList([u'Please upload a valid MP3.'])
                self._errors["mp3"] = errors
                del cleaned_data["mp3"]
            else:
                audio = EasyID3(self.files['mp3'].temporary_file_path())
                audio['title'] = cleaned_data['title']
                audio['artist'] = unicode(cleaned_data['speaker'])

                if not cleaned_data['series']:
                    album_title = 'Sermons from %s' % conf.KANISA_CHURCH_NAME
                else:
                    album_title = unicode(cleaned_data['series'])
                audio['album'] = album_title

                audio['albumartistsort'] = conf.KANISA_CHURCH_NAME
                audio['organization'] = conf.KANISA_CHURCH_NAME
                audio['genre'] = 'Speech'

                # Not sure if this date format is right - the MP3
                # players I've got to test with don't show anything
                # more than the year.
                audio['date'] = cleaned_data['date'].strftime('%Y%m%d')

                audio.save()

        return cleaned_data


class DocumentForm(KanisaBaseForm):
    class Meta:
        model = Document
        widgets = {'details': EpicWidget(), }


class ScheduledTweetForm(KanisaBaseForm):
    date = BootstrapDateField()
    time = BootstrapTimeField()

    def clean(self):
        cleaned_data = super(ScheduledTweetForm, self).clean()

        if self.instance.pk:
            return cleaned_data

        thedate = cleaned_data.get("date")
        thetime = cleaned_data.get("time")

        thedt = datetime.combine(thedate, thetime)
        if thedt < datetime.now():
            raise forms.ValidationError('You cannot scheduled tweets in the '
                                        'past.')

        return cleaned_data

    class Meta:
        model = ScheduledTweet
        exclude = ('posted', )


class KanisaLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Login'
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))

        super(KanisaLoginForm, self).__init__(*args, **kwargs)
