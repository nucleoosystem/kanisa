from kanisa.forms import KanisaBaseForm
from kanisa.forms.widgets import KanisaMainInputWidget
from kanisa.models import Block


class BlockForm(KanisaBaseForm):
    class Meta:
        model = Block
        widgets = {'contents': KanisaMainInputWidget(), }
        fields = ('contents', )
