from kanisa.forms import KanisaBaseForm
from kanisa.models import NavigationElement


class NavigationElementForm(KanisaBaseForm):
    class Meta:
        model = NavigationElement
