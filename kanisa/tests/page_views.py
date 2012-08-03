from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class PageManagementViewTest(KanisaViewTestCase):
    fixtures = ['pages.json', ]

    def test_views_protected(self):
        self.view_is_restricted(reverse('kanisa_manage_pages'))
        self.view_is_restricted(reverse('kanisa_manage_pages_create'))

        # This would 404 if you were logged in
        self.view_is_restricted(reverse('kanisa_manage_pages_update',
                                        args=[1, ]))

    def test_index_view(self):
        self.client.login(username='fred', password='secret')
        resp = self.client.get(reverse('kanisa_manage_pages'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/pages/index.html')
        self.client.logout()

    def test_create_page_view(self):
        self.client.login(username='fred', password='secret')

        url = reverse('kanisa_manage_pages_create')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/create.html')

        # Should 404 with an invalid ID
        resp = self.client.get(url + '?parent=foo')
        self.assertEqual(resp.status_code, 404)

        # Should 404 with a valid ID, which is non-existent
        resp = self.client.get(url + '?parent=99')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(url + '?parent=1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form'].initial['parent'].pk, 1)

        self.client.logout()

    def test_delete_page_view(self):
        self.client.login(username='fred', password='secret')

        # Can't delete pages which aren't root nodes
        resp = self.client.get(reverse('kanisa_manage_pages_delete',
                                       args=[1, ]))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.post(reverse('kanisa_manage_pages_delete',
                                        args=[1, ]),
                                {})
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(reverse('kanisa_manage_pages_delete',
                                       args=[2, ]))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse('kanisa_manage_pages_delete',
                                        args=[2, ]),
                                {},
                                follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [u'Staff deleted.', ])

        self.client.logout()
