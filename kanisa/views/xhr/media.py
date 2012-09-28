from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from kanisa.models import InlineImage, Document
from kanisa.views.xhr.base import XHRBaseGetView


class InlineImagesListView(XHRBaseGetView):
    permission = 'kanisa.manage_media'

    def render(self, request, *args, **kwargs):
        images = InlineImage.objects.all()
        tmpl = 'kanisa/management/media/_inline_image_list.html'
        return render_to_response(tmpl,
                                  {'object_list': images},
                                  context_instance=RequestContext(request))


class InlineImagesDetailView(XHRBaseGetView):
    permission = 'kanisa.manage_media'

    def render(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        image = get_object_or_404(InlineImage, pk=pk)

        tmpl = 'kanisa/management/media/_inline_image_detail.html'
        return render_to_response(tmpl,
                                  {'image': image},
                                  context_instance=RequestContext(request))


class AttachmentsListView(XHRBaseGetView):
    permission = 'kanisa.manage_media'

    def render(self, request, *args, **kwargs):
        documents = Document.objects.all()
        tmpl = 'kanisa/management/media/_attachment_list.html'
        return render_to_response(tmpl,
                                  {'object_list': documents},
                                  context_instance=RequestContext(request))
