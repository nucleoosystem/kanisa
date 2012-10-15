from __future__ import absolute_import
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

    def to_python(self, value):
        if isinstance(value, BiblePassage):
            return value

        if not value:
            return None

        try:
            return to_passage(value)
        except InvalidPassage:
            # Shouldn't get here - since we've saved the BiblePassage
            # in a model.
            return None

    def get_prep_value(self, value):
        if not value:
            return None

        return unicode(value)

try:
    from south.modelsinspector import add_introspection_rules as air
    air([], ["^kanisa\.models\.bible\.db_field\.BiblePassageField"])
except ImportError:
    pass
