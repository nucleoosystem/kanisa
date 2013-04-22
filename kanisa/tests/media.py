from django.test import TestCase
from kanisa.models import InlineImage
import factory


class InlineImageFactory(factory.Factory):
    FACTORY_FOR = InlineImage
    title = factory.Sequence(lambda n: 'InlineImage Title #' + n)
    image = 'non_existent_image.jpg'


class InlineImageTest(TestCase):
    def test_unicode(self):
        inline_image = InlineImageFactory.build()
        self.assertEqual(unicode(inline_image), 'InlineImage Title #0')
