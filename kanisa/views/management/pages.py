from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from kanisa.forms.pages import PageForm
from kanisa.models import Page, NavigationElement
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaDeleteView,
                                  KanisaListView)


class PageBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Pages are for static content, such as information about '
                   'your Church.')
    kanisa_root_crumb = {'text': 'Pages',
                         'url': reverse_lazy('kanisa_manage_pages')}
    permission = 'kanisa.manage_pages'
    kanisa_nav_component = 'pages'


class PageIndexView(PageBaseView,
                    KanisaListView):
    model = Page
    queryset = Page.objects.all()

    template_name = 'kanisa/management/pages/index.html'
    kanisa_title = 'Manage Pages'
    kanisa_is_root_view = True
page_management = PageIndexView.as_view()


class PageCreateView(PageBaseView,
                     KanisaCreateView):
    form_class = PageForm
    kanisa_title = 'Create a Page'
    success_url = reverse_lazy('kanisa_manage_pages')

    def get_initial(self):
        initial = super(PageCreateView, self).get_initial()

        if 'parent' in self.request.GET:
            parent = self.request.GET['parent']
            try:
                initial['parent'] = Page.objects.get(pk=int(parent))
            except ValueError:
                raise Http404
            except Page.DoesNotExist:
                raise Http404

        return initial

    def get_message(self, instance):
        try:
            page_url = '/' + instance.get_path()
            element = NavigationElement.objects.get(url=page_url,
                                                    parent__isnull=False)
            return ('Page "%s" created (and added to the '
                    'site navigation under "%s").'
                    % (unicode(instance), element.parent.title))
        except NavigationElement.DoesNotExist:
            return 'Page "%s" created.' % unicode(instance)
page_create = PageCreateView.as_view()


class PageUpdateView(PageBaseView,
                     KanisaUpdateView):
    form_class = PageForm
    model = Page
    success_url = reverse_lazy('kanisa_manage_pages')

    def get_preview_url(self):
        return '/' + self.get_object().get_path()
page_update = PageUpdateView.as_view()


class PageDeleteView(PageBaseView,
                     KanisaDeleteView):
    model = Page

    def get_cancel_url(self):
        return reverse('kanisa_manage_pages')

    def get_success_url(self):
        message = '%s deleted.' % self.object
        messages.success(self.request, message)
        return reverse('kanisa_manage_pages')

    def get_object(self, queryset=None):
        rval = super(PageDeleteView, self).get_object(queryset)

        if not rval.is_leaf_node():
            raise Http404

        return rval
page_delete = PageDeleteView.as_view()
