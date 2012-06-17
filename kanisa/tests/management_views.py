from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class ManagementViewTests(KanisaViewTestCase):
    fixtures = ['banners.json', 'diary.json', ]

    def test_views_protected(self):
        self.check_staff_only(reverse('kanisa.views.manage'))
        self.check_staff_only(reverse('kanisa_manage_banners'))
        self.check_staff_only(reverse('kanisa_manage_banners_retire',
                                      args=[1, ]))
        self.check_staff_only(reverse('kanisa_manage_banners_create'))
        self.check_staff_only(reverse('kanisa_manage_banners_update',
                                      args=[1, ]))
        self.check_staff_only(reverse('kanisa_manage_diary'))

    def test_root_view(self):
        url = reverse('kanisa.views.manage')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/index.html')

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

    def test_diary_root_view(self):
        url = reverse('kanisa_manage_diary')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/diary/index.html')
        self.assertTrue('calendar' in resp.context)
        self.assertTrue('events_to_schedule' in resp.context)
        self.assertTrue(resp.context['events_to_schedule'])
        self.assertEqual(len(resp.context['calendar']), 7)
