from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from kanisa.models import InlineImage
from sorl.thumbnail import get_thumbnail
import markdown
import re


register = template.Library()


image_expression = re.compile(r'(!\[img-([0-9]+)'
                              '( (headline|medium))?'
                              '( (left|right))?\]'
                              '(\[(.+?)\])?)')


class ImageMatch(object):
    def __init__(self, match):
        self.full = match[0]
        pk = match[1]
        self.size = match[3]
        self.align = match[5]

        if not self.size:
            self.size = u'medium'

        if not self.align:
            self.align = u'left'

        self.alt = match[7]
        self.image = InlineImage.objects.get(pk=pk)

    def tag(self):
        if self.size == 'headline':
            thumbnail = get_thumbnail(self.image.image.file,
                                      '960x200',
                                      crop='center')
            style = ""
        elif self.size == 'medium':
            thumbnail = get_thumbnail(self.image.image.file, '260x260')
            if self.align == "left":
                style = "float: left; margin-right: 10px; margin-bottom: 10px;"
            else:
                style = "float: right; margin-left: 10px; margin-bottom: 10px;"

        return ('<img src="%s" alt="%s" class="img-polaroid" '
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


@register.filter(is_safe=True)
def kanisa_markdown(value):
    value = force_unicode(value)
    for image_match in get_images(value):
        value = value.replace(image_match.full, image_match.tag())

    return mark_safe(markdown.markdown(value,
                                       extensions=['nl2br', ]))
