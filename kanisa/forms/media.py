from kanisa.forms import KanisaBaseModelForm
from kanisa.forms.widgets import ThumbnailFileInput
from kanisa.models import InlineImage


class InlineImageForm(KanisaBaseModelForm):
    class Meta:
        model = InlineImage
        widgets = {'image': ThumbnailFileInput(180, 180), }
