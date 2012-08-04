from django.core.urlresolvers import reverse
from django.test import TestCase


class PublicViewTest(TestCase):
    fixtures = ['banners.json', ]

    def test_kanisa_root_view(self):
        url = reverse('kanisa.views.index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/index.html')

        self.assertTrue('banners' in resp.context)
        self.assertEqual([banner.pk for banner in resp.context['banners']],
                         [1, 2, 3, 5, ])
