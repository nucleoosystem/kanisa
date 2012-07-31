from __future__ import absolute_import
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.forms import util
from django.forms.widgets import TextInput
from .bible import to_passage, InvalidPassage


class BiblePassageWidget(TextInput):
    class Media:
        js = ('kanisa/js/biblefield.js', )


class BiblePassageFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        url = reverse_lazy('kanisa_xhr_biblepassage_check')
        attrs = {'data-validate-url': url, }

        defaults = {'widget': BiblePassageWidget(attrs=attrs)}
        defaults.update(kwargs)

        super(BiblePassageFormField, self).__init__(*args, **defaults)

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
            raise util.ValidationError(e)
