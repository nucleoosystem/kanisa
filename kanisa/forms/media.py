from kanisa.forms import KanisaBaseForm
from kanisa.models import InlineImage


class InlineImageForm(KanisaBaseForm):
    class Meta:
        model = InlineImage
