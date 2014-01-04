from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from kanisa.models import InlineImage, Document
from sorl.thumbnail import get_thumbnail
import markdown
import re


register = template.Library()


image_expression = re.compile(r'(!\[([A-Za-z0-9\-]+)'
                              '( (headline|medium|small))?'
                              '( (left|right))?\]'
                              '(\[(.+?)\])?)')


document_expression = re.compile(r'({@([A-Za-z0-9\-]+)})')


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
        if self.size == 'headline':
            thumbnail = get_thumbnail(self.image.image.file,
                                      '960x200',
                                      crop='center')
            style = ""
        else:
            style = "float: %s; margin-" % self.align

            if self.align == "left":
                style = style + "right"
            else:
                style = style + "left"

            style = style + ": 10px; margin-bottom: 10px;"

            if self.size == 'medium':
                thumbnail = get_thumbnail(self.image.image.file, '260x260')
            elif self.size == 'small':
                thumbnail = get_thumbnail(self.image.image.file, '174x174')

        return ('<img src="%s" alt="%s" class="img-thumbnail" '
                'height="%spx" width="%spx" style="%s"/>' % (thumbnail.url,
                                                             self.alt,
                                                             thumbnail.height,
                                                             thumbnail.width,
                                                             style))


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
        self.document = Document.objects.get(slug=match[1],
                                             public=True)

    def tag(self):
        return '<a href="%s">Download %s</a>' % (self.document.file.url,
                                                 self.document.title)


def get_documents(markdown_text):
    documents = []
    for match in document_expression.findall(markdown_text):
        try:
            documents.append(DocumentMatch(match))
        except Document.DoesNotExist:
            # Just ignore bad document pks
            pass

    return documents


@register.filter(is_safe=True)
def kanisa_markdown(value):
    value = force_unicode(value)

    for image_match in get_images(value):
        value = value.replace(image_match.full, image_match.tag())

    for document_match in get_documents(value):
        value = value.replace(document_match.full, document_match.tag())

    value = value.replace("####", "<br style=\"clear: both\" />")

    return mark_safe(markdown.markdown(value,
                                       extensions=['nl2br', ]))
