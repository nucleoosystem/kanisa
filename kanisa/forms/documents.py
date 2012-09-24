from kanisa.forms import KanisaBaseForm
from kanisa.models import Document


class DocumentForm(KanisaBaseForm):
    class Meta:
        model = Document
