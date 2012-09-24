from kanisa.forms import KanisaBaseForm
from kanisa.forms.widgets import (KanisaIntroInputWidget,
                                  KanisaMainInputWidget)
from kanisa.models import Page


class PageForm(KanisaBaseForm):
    class Meta:
        model = Page
        widgets = {'lead': KanisaIntroInputWidget(),
                   'contents': KanisaMainInputWidget(), }
