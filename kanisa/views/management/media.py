from django.core.urlresolvers import reverse_lazy
from kanisa.forms.media import InlineImageForm
from kanisa.models import InlineImage
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaListView)


class MediaBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Inline images allow you to give your content some '
                   'context.')
    kanisa_root_crumb = {'text': 'Media',
                         'url': reverse_lazy('kanisa_manage_media')}
    permission = 'kanisa.manage_media'
    kanisa_nav_component = 'media'


class MediaIndexView(MediaBaseView,
                     KanisaListView):
    model = InlineImage
    queryset = InlineImage.objects.all().order_by('-modified')

    template_name = 'kanisa/management/media/index.html'
    kanisa_title = 'Manage Media'
    kanisa_is_root_view = True
    paginate_by = 24

media_management = MediaIndexView.as_view()


class InlineImageCreateView(MediaBaseView,
                            KanisaCreateView):
    form_class = InlineImageForm
    kanisa_title = 'Upload an Inline Image'
    success_url = reverse_lazy('kanisa_manage_media')
media_inline_image_create = InlineImageCreateView.as_view()


class InlineImageUpdateView(MediaBaseView,
                            KanisaUpdateView):
    form_class = InlineImageForm
    model = InlineImage
    success_url = reverse_lazy('kanisa_manage_media')
media_inline_image_update = InlineImageUpdateView.as_view()
