from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from kanisa.models import InlineImage, Document
from kanisa.views.xhr.base import XHRBaseGetView


class PaginatedListView(object):
    results_per_page = 8

    def slice_results(self, request, results):
        try:
            page_no = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        paginator = Paginator(results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)


class InlineImagesListView(PaginatedListView, XHRBaseGetView):
    permission = 'kanisa.manage_media'

    def render(self, request, *args, **kwargs):
        images = InlineImage.objects.all()
        paginator, page = self.slice_results(request, images)
        tmpl = 'kanisa/management/media/_inline_image_list.html'

        return render_to_response(tmpl,
                                  {'page_obj': page},
                                  context_instance=RequestContext(request))
list_inline_images = InlineImagesListView.as_view()


class InlineImagesDetailView(XHRBaseGetView):
    permission = 'kanisa.manage_media'

    def render(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        image = get_object_or_404(InlineImage, pk=pk)

        tmpl = 'kanisa/management/media/_inline_image_detail.html'
        return render_to_response(tmpl,
                                  {'image': image},
                                  context_instance=RequestContext(request))
inline_image_detail = InlineImagesDetailView.as_view()


class AttachmentsListView(PaginatedListView, XHRBaseGetView):
    permission = 'kanisa.manage_media'

    def render(self, request, *args, **kwargs):
        documents = Document.objects.filter(public=True)
        paginator, page = self.slice_results(request, documents)
        tmpl = 'kanisa/management/media/_attachment_list.html'

        return render_to_response(tmpl,
                                  {'page_obj': page},
                                  context_instance=RequestContext(request))
list_attachments = AttachmentsListView.as_view()
