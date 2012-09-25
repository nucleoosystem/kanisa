from django.forms import Textarea, TextInput
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


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
    class Media:
        js = ('kanisa/js/main_input_widget.js', )

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, name=name)

        return render_to_string("kanisa/management/_main_input_widget.html",
                                {'attrs': mark_safe(flatatt(final_attrs)),
                                 'id': final_attrs['id'],
                                 'value': value})
