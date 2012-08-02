from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class EpicWidget(forms.Textarea):
    class Media:
        js = ('kanisa/epiceditor/js/epiceditor.js', )

    def __init__(self, *args, **kwargs):
        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}

        super(EpicWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, name=name)

        escaped = conditional_escape(force_unicode(value))
        output = render_to_string('kanisa/management/_epic_widget.html',
                                  {'id': final_attrs["id"],
                                   'name': final_attrs["name"],
                                   'value': escaped, })
        return mark_safe(output)
