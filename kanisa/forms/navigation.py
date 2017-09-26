from kanisa.forms import KanisaBaseModelForm
from kanisa.models import NavigationElement


class NavigationElementForm(KanisaBaseModelForm):
    class Meta:
        model = NavigationElement
        fields = (
            'title',
            'alternate_title',
            'description',
            'url',
            'parent',
            'require_login',
        )
