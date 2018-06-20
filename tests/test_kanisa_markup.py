import factory
import os
import pytest
import re

from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Context, Template

from kanisa.models import InlineImage
from kanisa.templatetags.kanisa_markup import kanisa_markdown


test_image_path = os.path.join(
    os.path.dirname(__file__), 'assets', 'example.jpg'
)


class InlineImageFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'InlineImage Title #%d' % n)
    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open(test_image_path, 'rb').read(),
        content_type="image/jpeg"
    )

    class Meta:
        model = InlineImage


def ws_remove(val):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', val)


def test_basic_markup():
    assert kanisa_markdown("hello") == '<p>hello</p>'


def test_newlines():
    result = kanisa_markdown("hello\nworld")
    assert ws_remove(result) == '<p>hello<br/>world</p>'
    result = kanisa_markdown("hello\n\nworld")
    assert ws_remove(result) == '<p>hello</p><p>world</p>'


@pytest.mark.django_db
def test_inline_image_that_does_not_exist():
    result = kanisa_markdown("hello ![img-99 headline]")
    assert result == '<p>hello ![img-99 headline]</p>'


@pytest.mark.django_db
def test_inline_image_that_does_exist():
    inline_image = InlineImageFactory.create()
    result = kanisa_markdown("hello ![%s headline]" % inline_image.slug)
    assert '<p>hello <img src="' in result
    expected_classes = ' '.join([
        'img-thumbnail',
        'inline-image-base',
        'inline-image-headline',
    ])
    tail = ('alt="" class="%s" height="200px" width="960px" /></p>'
            % expected_classes)
    assert tail in result


def test_headings():
    test_input = "# Heading 1\n## Heading 2"
    test_output = "<h1>Heading 1</h1>\n<h2>Heading 2</h2>"
    template = Template("{% load kanisa_markup %}{{ input|kanisa_markdown }}")
    assert test_output == template.render(Context({'input': test_input }))


def test_headings_demoted_one_level():
    test_input = "# Heading 1\n## Heading 2"
    test_output = "<h2>Heading 1</h2>\n<h3>Heading 2</h3>"
    template = Template("{% load kanisa_markup %}{{ input|kanisa_markdown:1 }}")
    assert test_output == template.render(Context({'input': test_input }))


def test_headings_demoted_two_levels():
    test_input = "# Heading 1\n## Heading 2"
    test_output = "<h3>Heading 1</h3>\n<h4>Heading 2</h4>"
    template = Template("{% load kanisa_markup %}{{ input|kanisa_markdown:2 }}")
    assert test_output == template.render(Context({'input': test_input }))


def test_newline_to_break():
    test_input = "Line 1\nLine 2"
    test_output = "<p>Line 1<br />\nLine 2</p>"
    template = Template("{% load kanisa_markup %}{{ input|kanisa_markdown }}")
    assert test_output == template.render(Context({'input': test_input }))


@pytest.mark.django_db
def test_inline_image_with_template():
    inline_image = InlineImageFactory.create()
    test_input = "hello ![%s medium]" % inline_image.slug
    template = Template("{% load kanisa_markup %}{{ input|kanisa_markdown }}")
    test_output = template.render(Context({'input': test_input }))
    assert "<p>hello <img" in test_output
