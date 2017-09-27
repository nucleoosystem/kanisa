from crispy_forms.bootstrap import InlineCheckboxes
from django.forms import Textarea, TextInput
from django.forms.utils import flatatt
from django.forms.widgets import (
    ClearableFileInput,
    DateInput,
    SelectMultiple,
    TimeInput,
)
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from sorl.thumbnail.shortcuts import get_thumbnail


TIMEPICKER_FORMAT = '%I:%M %p'


class KanisaTinyInputWidget(TextInput):
    pass


class KanisaIntroInputWidget(Textarea):
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'cols': '40', 'rows': '2'}
        if attrs:
            default_attrs.update(attrs)
        super(KanisaIntroInputWidget, self).__init__(default_attrs)


class KanisaMainInputWidget(Textarea):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, name=name)

        return render_to_string("kanisa/management/_main_input_widget.html",
                                {'attrs': mark_safe(flatatt(final_attrs)),
                                 'id': final_attrs['id'],
                                 'value': value})


class KanisaThumbnailFileWidget(ClearableFileInput):
    template_with_initial = ('%(initial)s %(clear_template)s<br />'
                             '%(input_text)s: %(input)s')

    def __init__(self, width, height, attrs=None):
        self.dimensions = {
            'width': width,
            'height': height
        }

        super(KanisaThumbnailFileWidget, self).__init__(attrs)

    @property
    def url_markup_template(self):
        thumbnail = get_thumbnail(self.thumbnail_url,
                                  "%(width)dx%(height)d" % self.dimensions)
        return '<img src="%s" /><br />' % thumbnail.url

    def render(self, name, value, attrs=None):
        self.thumbnail_url = value

        return super(KanisaThumbnailFileWidget,
                     self).render(name, value, attrs)


class KanisaInlineCheckboxes(InlineCheckboxes):
    template = "kanisa/management/_checkboxselectmultiple.html"


class BootstrapTimeWidget(TimeInput):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = TIMEPICKER_FORMAT
        extra_attrs = {'data-provide': 'timepicker',
                       'class': 'timepicker'}

        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}

        kwargs['attrs'].update(extra_attrs)

        super(BootstrapTimeWidget, self).__init__(*args, **kwargs)


class BootstrapDateWidget(DateInput):
    def __init__(self, *args, **kwargs):
        extra_attrs = {'data-date-format': 'dd/mm/yyyy',
                       'class': 'datepicker'}

        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}

        kwargs['attrs'].update(extra_attrs)

        super(BootstrapDateWidget, self).__init__(*args, **kwargs)


class KanisaAccountMultipleSelector(SelectMultiple):
    pass


class KanisaBlogTeaserInputWidget(KanisaMainInputWidget):
    pass
