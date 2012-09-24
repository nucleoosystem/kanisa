from django.forms.util import ErrorList

from kanisa import conf
from kanisa.forms import KanisaBaseForm, BootstrapDateField
from kanisa.forms.widgets import KanisaMainInputWidget
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError, TIT2

from kanisa.models import (SermonSeries,
                           Sermon,
                           SermonSpeaker)


class SermonSeriesForm(KanisaBaseForm):
    class Meta:
        model = SermonSeries
        widgets = {'details': KanisaMainInputWidget(), }


class SermonSpeakerForm(KanisaBaseForm):
    class Meta:
        model = SermonSpeaker


class SermonForm(KanisaBaseForm):
    date = BootstrapDateField()

    class Meta:
        model = Sermon
        widgets = {'details': KanisaMainInputWidget(), }

    def apply_id3(self, cleaned_data):
        try:
            audio = EasyID3(self.files['mp3'].temporary_file_path())
        except ID3NoHeaderError:
            audio = MP3(self.files['mp3'].temporary_file_path())
            audio["TIT2"] = TIT2(encoding=3, text=[cleaned_data['title']])
            audio.save()
            audio = EasyID3(self.files['mp3'].temporary_file_path())

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

        # Not sure if this date format is right - the MP3 players I've
        # got to test with don't show anything more than the year.
        audio['date'] = cleaned_data['date'].strftime('%Y%m%d')

        audio.save()

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

            if audio is None or not audio.info or audio.info.sketchy:
                errors = ErrorList([u'Please upload a valid MP3.'])
                self._errors["mp3"] = errors
                del cleaned_data["mp3"]
            else:
                self.apply_id3(cleaned_data)

        return cleaned_data
