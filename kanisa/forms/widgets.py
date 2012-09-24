from django.forms import Textarea, TextInput


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
    pass
