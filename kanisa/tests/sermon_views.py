from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class SermonManagementViewTest(KanisaViewTestCase):
    fixtures = ['sermons.json', ]

    def test_views_protected(self):
        prefix = 'kanisa_manage_sermons'
        self.check_staff_only_302(reverse(prefix))
        self.check_staff_only_302(reverse('%s_series_create' % prefix))
        self.check_staff_only_302(reverse('%s_individual_create' % prefix))
        self.check_staff_only_302(reverse('%s_speaker' % prefix))
        self.check_staff_only_302(reverse('%s_speaker_create' % prefix))

        self.check_staff_only_302(reverse('%s_series_detail' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_series_update' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_series_complete' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_individual_update' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_speaker_update' % prefix,
                                          args=[1, ]))

    def test_index_view(self):
        self.client.login(username='fred', password='secret')
        resp = self.client.get(reverse('kanisa_manage_sermons'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/sermons/index.html')

        self.assertEqual(len(resp.context['standalone']), 1)
        self.assertEqual(len(resp.context['object_list']), 3)
        self.client.logout()

    def test_create_series_view(self):
        self.client.login(username='fred', password='secret')

        resp = self.client.get(reverse('kanisa_manage_sermons_series_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/create.html')

        self.client.logout()

    def test_create_series_view(self):
        self.client.login(username='fred', password='secret')
        base_url = reverse('kanisa_manage_sermons_individual_create')

        # Check with a pre-populated series
        url = '%s?series=2' % base_url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/create.html')
        self.assertEqual(resp.context['form'].initial['series'], '2')

        # Check without a pre-populated series
        resp = self.client.get(base_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/create.html')
        self.assertTrue('series' not in resp.context['form'].initial)

        # Check with an invalid pre-populated series
        url = '%s?series=foobar' % base_url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/create.html')
        self.assertEqual(resp.context['form'].initial['series'], 'foobar')

        self.client.logout()

    def test_create_speaker_view(self):
        self.client.login(username='fred', password='secret')

        resp = self.client.get(reverse('kanisa_manage_sermons_speaker_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/create.html')

        self.client.logout()
