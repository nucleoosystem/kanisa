from kanisa.models import RegisteredUser
from kanisa.forms import KanisaBaseModelForm
from .widgets import ThumbnailFileInput


class UserUpdateForm(KanisaBaseModelForm):
    class Meta:
        fields = ('first_name', 'last_name', 'email', 'image', )
        model = RegisteredUser
        widgets = {'image': ThumbnailFileInput(), }
