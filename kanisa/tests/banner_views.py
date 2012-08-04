from django.core.urlresolvers import reverse
from kanisa.models import Banner
from kanisa.tests.utils import KanisaViewTestCase
from django.test import TestCase


class BannerManagementViewTest(KanisaViewTestCase):
    fixtures = ['banners.json', ]

    def test_views_protected(self):
        self.view_is_restricted(reverse('kanisa_manage_banners'))
        self.view_is_restricted(reverse('kanisa_manage_banners_retire',
                                        args=[1, ]))
        self.view_is_restricted(reverse('kanisa_manage_banners_create'))
        self.view_is_restricted(reverse('kanisa_manage_banners_update',
                                        args=[1, ]))

    def test_banner_management_view(self):
        url = reverse('kanisa_manage_banners')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/banners/index.html')

        self.assertTrue('banner_list' in resp.context)
        self.assertEqual([banner.pk for banner in resp.context['banner_list']],
                         [1, 2, 3, 5, ])

    def test_banner_retire_view(self):
        url = reverse('kanisa_manage_banners_retire', args=[1, ])
        self.client.login(username='fred', password='secret')

        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('banner_list' in resp.context)
        self.assertEqual([banner.pk for banner in resp.context['banner_list']],
                         [2, 3, 5, ])

        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [u'Banner "Green Flowers" retired.', ])

    def test_banner_create_view_required_fields(self):
        url = reverse('kanisa_manage_banners_create')
        self.client.login(username='fred', password='secret')
        resp = self.client.post(url, {})
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'headline',
                             'This field is required.')
        self.assertFormError(resp, 'form', 'image',
                             'This field is required.')


class BannerPublicViewTest(TestCase):
    fixtures = ['banners.json', ]

    def test_banner_visit_counting(self):
        banner = Banner.objects.get(pk=2)
        self.assertEqual(banner.url, "http://www.google.com")
        self.assertEqual(banner.visits, 0)

        url = reverse('kanisa_public_banners_visit', args=[banner.pk, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        items = resp.items()
        self.assertEqual(items[-1],
                         ('Location', 'http://www.google.com'))

        banner = Banner.objects.get(pk=2)
        self.assertEqual(banner.visits, 1)

    def test_banner_visit_counting_404s_without_url(self):
        banner = Banner.objects.get(pk=1)
        self.assertEqual(banner.url, '')
        url = reverse('kanisa_public_banners_visit', args=[banner.pk, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
