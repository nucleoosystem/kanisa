from django.core.urlresolvers import reverse
from kanisa.models import Page
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

        resp = self.client.post(url, {'title': "Test page"},
                                follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [u'Page "Test page" created.', ])

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

        resp = self.client.post(reverse('kanisa_manage_pages_delete',
                                        args=[3, ]),
                                {},
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, '"Location" deleted')

        self.client.logout()

    def test_update_page_view(self):
        self.client.login(username='fred', password='secret')

        p = Page.objects.get(pk=1)
        url = reverse('kanisa_manage_pages_update', args=[1, ])

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(url, {'title': p.title,
                                      'contents': p.contents},
                                follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [u'Page "%s" saved.' % p.title, ])

        # Pages cannot be their own parents
        resp = self.client.post(url, {'title': p.title,
                                      'contents': p.contents,
                                      'parent': p.pk})
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'parent',
                             'A page cannot be its own parent.')

        # Pages cannot have their descendants as their parent
        child = Page.objects.get(pk=4)
        self.assertEqual(child.parent, p)
        resp = self.client.post(url, {'title': p.title,
                                      'contents': p.contents,
                                      'parent': child.pk})
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'parent',
                             'Invalid parent - cyclical hierarchy detected.')

        url = reverse('kanisa_manage_pages_update', args=[4, ])
        resp = self.client.post(url, {'title': child.title,
                                      'contents': child.contents,
                                      'parent': 2})
        self.assertEqual(resp.status_code, 302)

        self.client.logout()
