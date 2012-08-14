from django.core.urlresolvers import reverse
from django.test import TestCase
from kanisa.models import Banner
import factory


class BannerFactory(factory.Factory):
    FACTORY_FOR = Banner
    headline = factory.Sequence(lambda n: 'Banner Title #' + n)
    contents = 'Banner contents'
    image = 'non_existent_image.jpg'


class PublicViewTest(TestCase):
    def test_kanisa_root_view(self):
        banner1 = BannerFactory.create()
        banner2 = BannerFactory.create()
        banner3 = BannerFactory.create()
        banner4 = BannerFactory.create()
        banner5 = BannerFactory.create()
        banner4.set_retired()

        url = reverse('kanisa.views.index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/index.html')

        self.assertTrue('banners' in resp.context)
        self.assertEqual([banner.pk for banner in resp.context['banners']],
                         [banner1.pk, banner2.pk, banner3.pk, banner5.pk, ])
