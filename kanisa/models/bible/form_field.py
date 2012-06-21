from __future__ import absolute_import
from django import forms
from django.forms import util
from .bible import to_passage, InvalidPassage


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
            return unicode(to_passage(value))
        except InvalidPassage, e:
            raise util.ValidationError(('\'%s\' is not a valid Bible '
                                        'reference. %s') % (value, e))
