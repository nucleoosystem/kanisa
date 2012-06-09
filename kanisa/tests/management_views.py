from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class ManagementViewTests(KanisaViewTestCase):
    fixtures = ['banners.json', ]

    def test_views_protected(self):
        self.check_staff_only(reverse('kanisa.views.manage'))
        self.check_staff_only(reverse('kanisa.views.manage_banners'))
        self.check_staff_only(reverse('kanisa.views.retire_banner',
                                      args=[1, ]))
        self.check_staff_only(reverse('kanisa_create_banner'))
        self.check_staff_only(reverse('kanisa_update_banner',
                                      args=[1, ]))

    def test_root_view(self):
        url = reverse('kanisa.views.manage')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/index.html')

    def test_banner_management_view(self):
        url = reverse('kanisa.views.manage_banners')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/banners/index.html')

        self.assertTrue('banners' in resp.context)
        self.assertEqual([banner.pk for banner in resp.context['banners']],
                         [1, 2, 3, 5, ])

    def test_banner_retire_view(self):
        url = reverse('kanisa.views.retire_banner', args=[1, ])
        self.client.login(username='fred', password='secret')

        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('banners' in resp.context)
        self.assertEqual([banner.pk for banner in resp.context['banners']],
                         [2, 3, 5, ])

        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [u'Banner "Green Flowers" retired.', ])
