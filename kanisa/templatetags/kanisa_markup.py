from django import template
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from kanisa.models import InlineImage, Document
from kanisa.utils.text import demote_headings
from sorl.thumbnail import get_thumbnail
import logging
import markdown
import re


logger = logging.getLogger(__name__)

register = template.Library()


image_expression = re.compile(r'(!\[([A-Za-z0-9\-_]+)'
                              '( (headline|medium|small|full))?'
                              '( (left|right))?\]'
                              '(\[(.+?)\])?)')


document_expression = re.compile(r'({@([A-Za-z0-9\-_]+)})')
gmap_expression = re.compile(r'({gmap:([a-z0-9\.]+)})')


class ImageMatch(object):
    def __init__(self, match):
        self.full = match[0]
        slug = match[1]
        self.size = match[3]
        self.align = match[5]

        if not self.size:
            self.size = 'medium'

        if not self.align:
            self.align = 'left'

        self.alt = match[7]
        self.image = InlineImage.objects.get(slug=slug)

    def tag(self):

        klasses = [
            'img-thumbnail',
            'inline-image-base',
            'inline-image-%s' % self.size,
        ]

        if self.size == 'headline':
            thumbnail = get_thumbnail(self.image.image.file,
                                      '960x200',
                                      crop='center')
        else:
            klasses.append('inline-image-align-%s' % self.align)

            if self.size == 'medium':
                thumbnail = get_thumbnail(self.image.image.file, '260x260')
            elif self.size == 'small':
                thumbnail = get_thumbnail(self.image.image.file, '174x174')
            elif self.size == 'full':
                thumbnail = self.image.image

        return ('<img src="%s" alt="%s" class="%s" '
                'height="%spx" width="%spx" />' % (
                    thumbnail.url,
                    self.alt,
                    ' '.join(klasses),
                    thumbnail.height,
                    thumbnail.width,
                ))


def get_images(markdown_text):
    images = []
    for match in image_expression.findall(markdown_text):
        try:
            images.append(ImageMatch(match))
        except InlineImage.DoesNotExist:
            # Just ignore bad image names
            pass

    return images


class DocumentMatch(object):
    def __init__(self, match):
        self.full = match[0]
        self.missing_reason = None
        self.document = None

        try:
            self.document = Document.objects.get(slug=match[1])
            if self.document.has_expired():
                logger.error(
                    'Tried to load expired document with slug %s' % match[1]
                )
                self.document = None
                self.missing_reason = 'expired'
        except Document.DoesNotExist:
            logger.error(
                'Tried to load non-existent document with slug %s' % match[1]
            )

            self.document = None
            self.missing_reason = 'not_found'

    def tag(self):
        return render_to_string(
            "kanisa/_download.html",
            {
                'document': self.document,
                'missing_reason': self.missing_reason,
            }
        )


class MapMatch(object):
    def __init__(self, match):
        self.full = match[0]
        self.msid = match[1]

    def tag(self):
        return render_to_string("kanisa/public/_google_map.html",
                                {'msid': self.msid})


def get_documents(markdown_text):
    documents = []
    for match in document_expression.findall(markdown_text):
        documents.append(DocumentMatch(match))

    return documents


def get_maps(markdown_text):
    maps = []

    for match in gmap_expression.findall(markdown_text):
        maps.append(MapMatch(match))

    return maps


@register.filter(is_safe=True)
def kanisa_markdown(value, demote_heading_levels=None):
    value = force_unicode(value)

    for image_match in get_images(value):
        value = value.replace(image_match.full, image_match.tag())

    for document_match in get_documents(value):
        value = value.replace(document_match.full, document_match.tag())

    for map_match in get_maps(value):
        value = value.replace(map_match.full, map_match.tag())

    value = value.replace("####", "<br style=\"clear: both\" />")

    marked_down = markdown.markdown(
        value,
        extensions=['markdown.extensions.nl2br', ]
    )

    if demote_heading_levels:
        marked_down = demote_headings(marked_down, demote_heading_levels)

    return mark_safe(marked_down)
