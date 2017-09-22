from kanisa.forms import KanisaBaseModelForm, BootstrapDateField
from kanisa.forms.widgets import KanisaMainInputWidget

from kanisa.models import SiteWideNotice


class SiteWideNoticeForm(KanisaBaseModelForm):
    publish_until = BootstrapDateField()

    class Meta:
        fields = [
            'headline',
            'publish_until',
            'contents',
        ]
        model = SiteWideNotice
        widgets = {
            'contents': KanisaMainInputWidget()
        }


class SiteWideNoticeEditForm(KanisaBaseModelForm):
    publish_until = BootstrapDateField()

    class Meta:
        fields = [
            'headline',
            'published',
            'publish_until',
            'contents',
        ]
        model = SiteWideNotice
        widgets = {
            'contents': KanisaMainInputWidget()
        }
