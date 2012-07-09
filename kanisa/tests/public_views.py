from django.core.urlresolvers import reverse
from kanisa.models import Banner
from kanisa.tests.utils import KanisaViewTestCase


class PublicViewTest(KanisaViewTestCase):
    fixtures = ['banners.json', ]

    def test_kanisa_root_view(self):
        url = reverse('kanisa.views.index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/index.html')

        self.assertTrue('banners' in resp.context)
        self.assertEqual([banner.pk for banner in resp.context['banners']],
                         [1, 2, 3, 5, ])

    def test_banner_visit_counting(self):
        banner = Banner.objects.get(pk=2)
        self.assertEqual(banner.url, "http://www.google.com")
        self.assertEqual(banner.visits, 0)

        url = reverse('kanisa_public_banners_visit', args=[banner.pk, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        items = resp.items()
        self.assertEqual(len(items), 3)
        self.assertEqual(items[2],
                         ('Location', 'http://www.google.com'))

        banner = Banner.objects.get(pk=2)
        self.assertEqual(banner.visits, 1)

    def test_banner_visit_counting_404s_without_url(self):
        banner = Banner.objects.get(pk=1)
        self.assertEqual(banner.url, '')
        url = reverse('kanisa_public_banners_visit', args=[banner.pk, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
