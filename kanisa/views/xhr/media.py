from django.shortcuts import render_to_response
from django.template import RequestContext

from kanisa.models import InlineImage
from kanisa.views.xhr.base import XHRBaseGetView


class InlineImagesListView(XHRBaseGetView):
    permission = 'kanisa.manage_media'

    def render(self, request, *args, **kwargs):
        images = InlineImage.objects.all()
        tmpl = 'kanisa/management/media/_inline_image_list.html'
        return render_to_response(tmpl,
                                  {'object_list': images},
                                  context_instance=RequestContext(request))
