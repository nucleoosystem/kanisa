import pytest
import re

from kanisa.templatetags.kanisa_markup import kanisa_markdown


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
