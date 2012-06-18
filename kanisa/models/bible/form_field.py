from django import forms
from django.forms import util
from kanisa.models.bible import bible


class BiblePassageFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(BiblePassageFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Validates that the input is a valid BiblePassage. Returns a
        Unicode object.
        """
        value = super(BiblePassageFormField, self).clean(value)
        if value == u'':
            return value

        try:
            return unicode(bible.to_passage(value))
        except bible.InvalidPassage, e:
            raise util.ValidationError(u('\'%s\' is not a valid Bible '
                                         'reference. %s') % (value, e))
