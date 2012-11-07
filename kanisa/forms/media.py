from kanisa.forms import KanisaBaseModelForm
from kanisa.models import InlineImage


class InlineImageForm(KanisaBaseModelForm):
    class Meta:
        model = InlineImage
