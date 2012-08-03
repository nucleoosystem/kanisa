from kanisa.forms import KanisaBaseForm
from kanisa.widgets import EpicWidget
from kanisa.models import Document


class DocumentForm(KanisaBaseForm):
    class Meta:
        model = Document
        widgets = {'details': EpicWidget(), }
