from kanisa.forms import KanisaBaseModelForm
from kanisa.forms.widgets import KanisaMainInputWidget
from kanisa.models import Document


class DocumentForm(KanisaBaseModelForm):
    class Meta:
        model = Document
        widgets = {'details': KanisaMainInputWidget(), }
        fields = (
            'title',
            'file',
            'details',
            'public',
        )


class DocumentFormSimple(KanisaBaseModelForm):
    class Meta:
        model = Document
        fields = (
            'title',
            'file',
        )
