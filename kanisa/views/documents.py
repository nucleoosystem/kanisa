from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet
from kanisa.forms.documents import DocumentForm
from kanisa.models import Document
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaDeleteView,
                                  KanisaTemplateView)


class DocumentBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Storing documents on your site allows people to have '
                   'easy access to the files they need.')
    kanisa_root_crumb = {'text': 'Documents',
                         'url': reverse_lazy('kanisa_manage_documents')}
    permission = 'kanisa.manage_documents'
    kanisa_nav_component = 'documents'


class DocumentIndexView(DocumentBaseView,
                        KanisaListView):
    model = Document
    queryset = Document.objects.all()

    template_name = 'kanisa/management/documents/index.html'
    kanisa_title = 'Manage Documents'
    kanisa_is_root_view = True


class DocumentSearchView(DocumentBaseView,
                         KanisaTemplateView):
    kanisa_title = 'Search Documents'
    template_name = 'kanisa/management/documents/search.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('kanisa_manage_documents'))

    def post(self, request, *args, **kwargs):
        query = request.POST.get('query', None)

        if not query:
            messages.warning(self.request, 'No search query entered.')
            return HttpResponseRedirect(reverse('kanisa_manage_documents'))

        matching = SearchQuerySet().models(Document).\
            filter(content=request.POST['query'])

        context = self.get_context_data(**kwargs)
        context['results'] = matching
        context['search_term'] = query

        return render_to_response(self.template_name,
                                  context,
                                  context_instance=RequestContext(request))


class DocumentCreateView(DocumentBaseView,
                         KanisaCreateView):
    form_class = DocumentForm
    kanisa_title = 'Upload a Document'
    success_url = reverse_lazy('kanisa_manage_documents')


class DocumentUpdateView(DocumentBaseView,
                         KanisaUpdateView):
    form_class = DocumentForm
    model = Document
    success_url = reverse_lazy('kanisa_manage_documents')


class DocumentDeleteView(DocumentBaseView,
                         KanisaDeleteView):
    model = Document

    def get_cancel_url(self):
        return reverse('kanisa_manage_documents')

    def get_success_url(self):
        message = '%s deleted.' % self.object
        messages.success(self.request, message)
        return reverse('kanisa_manage_documents')
