from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from kanisa.forms.blocks import BlockForm
from kanisa.models import Block
from kanisa.models.blocks import KNOWN_BLOCKS
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaUpdateView,
                                  KanisaTemplateView)


class BlockBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Content blocks are fragments of pages that can be '
                   'configured.')
    kanisa_root_crumb = {'text': 'Content Blocks',
                         'url': reverse_lazy('kanisa_manage_blocks')}
    permission = 'kanisa.manage_blocks'
    kanisa_nav_component = 'blocks'


class BlockIndexView(BlockBaseView,
                     KanisaTemplateView):
    template_name = 'kanisa/management/blocks/index.html'
    kanisa_title = 'Manage Blocks'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(BlockIndexView,
                        self).get_context_data(**kwargs)

        existing_blocks = dict((b.slug, b) for b in Block.objects.all())

        class BlockEntry(object):
            def __init__(self, slug, info, existing_blocks):
                self.slug = slug
                self.identifier = info[0]
                self.description = info[1]
                self.existing_block = existing_blocks.get(self.slug,
                                                          None)

        blocks = [BlockEntry(slug, info, existing_blocks)
                  for slug, info in KNOWN_BLOCKS.items()]

        context['blocks'] = blocks

        return context


class BlockUpdateView(BlockBaseView,
                      KanisaUpdateView):
    success_url = reverse_lazy('kanisa_manage_blocks')
    form_class = BlockForm
    model = Block

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get('slug', None)

        if slug is None:
            raise Http404('No slug found.')

        if slug not in KNOWN_BLOCKS:
            msg = 'Slug %s is not in the list of known blocks.' % slug
            raise Http404(msg)

        object = queryset.get_or_create(slug=slug)
        return object[0]
