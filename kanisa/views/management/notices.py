from datetime import date
from django.core.urlresolvers import reverse_lazy

from kanisa.forms.notices import (
    SiteWideNoticeForm,
    SiteWideNoticeEditForm
)
from kanisa.models import SiteWideNotice
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaCreateView,
    KanisaUpdateView,
    KanisaListView
)


class NoticeBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Notices give you a place to inform your users of '
                   'important news.')
    kanisa_root_crumb = {
        'text': 'Notices',
        'url': reverse_lazy('kanisa_manage_notices')
    }
    permission = 'kanisa.manage_notices'
    kanisa_nav_component = 'notices'


class NoticeManagementView(NoticeBaseView,
                           KanisaListView):
    model = SiteWideNotice
    template_name = 'kanisa/management/notices/index.html'
    kanisa_title = 'Manage the Notices'
    kanisa_is_root_view = True
notice_management = NoticeManagementView.as_view()


class NoticeCreateView(NoticeBaseView,
                       KanisaCreateView):
    model = SiteWideNotice
    form_class = SiteWideNoticeForm
    kanisa_title = 'Write a Notice'
    success_url = reverse_lazy('kanisa_manage_notices')

    def get_form(self, form_class):
        form = super(NoticeCreateView, self).get_form(form_class)
        form.initial = {
            'author': self.request.user,
            'publish_date': date.today()
        }
        return form
notice_create = NoticeCreateView.as_view()


class NoticeUpdateView(NoticeBaseView,
                       KanisaUpdateView):
    model = SiteWideNotice
    form_class = SiteWideNoticeEditForm
    success_url = reverse_lazy('kanisa_manage_notices')
notice_update = NoticeUpdateView.as_view()
