from django.core.urlresolvers import reverse_lazy
from kanisa.forms import PageForm
from kanisa.models import Page
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaListView)


class PageBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Pages are for static content, such as information about '
                   'your Church.')
    kanisa_root_crumb = {'text': 'Pages',
                         'url': reverse_lazy('kanisa_manage_pages')}
    permission = 'kanisa.manage_pages'


class PageIndexView(PageBaseView,
                    KanisaListView):
    model = Page
    queryset = Page.objects.all()

    template_name = 'kanisa/management/pages/index.html'
    kanisa_title = 'Manage Pages'
    kanisa_is_root_view = True


class PageCreateView(PageBaseView,
                     KanisaCreateView):
    form_class = PageForm
    kanisa_title = 'Create a Page'
    success_url = reverse_lazy('kanisa_manage_pages')


class PageUpdateView(PageBaseView,
                     KanisaUpdateView):
    form_class = PageForm
    model = Page
    success_url = reverse_lazy('kanisa_manage_pages')
