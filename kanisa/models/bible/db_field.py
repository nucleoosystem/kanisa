from __future__ import absolute_import
from django.core import exceptions
from django.db import models
from .bible import to_passage, InvalidPassage, BiblePassage
from .form_field import BiblePassageFormField


class BiblePassageField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 25
        super(BiblePassageField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': BiblePassageFormField}
        defaults.update(kwargs)

        return super(BiblePassageField, self).formfield(**defaults)

    def db_type(self, connection):
        return 'char(25)'

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        if isinstance(value, BiblePassage):
            return value

        # Parse a string into a BiblePassage object
        try:
            if not value or len(value) == 0:
                return None

            return to_passage(value)
        except InvalidPassage:
            raise exceptions.ValidationError

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, BiblePassage):
            return unicode(value)

        passage = self.to_python(value)

        if passage:
            return unicode(passage)

        return u''
