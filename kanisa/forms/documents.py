from kanisa.forms import KanisaBaseForm
from kanisa.forms.widgets import KanisaMainInputWidget
from kanisa.models import Document


class DocumentForm(KanisaBaseForm):
    class Meta:
        model = Document
        widgets = {'details': KanisaMainInputWidget(), }
