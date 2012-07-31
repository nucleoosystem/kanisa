from django.core.urlresolvers import reverse_lazy
from kanisa.tests.utils import KanisaViewTestCase


class XHRBiblePassageViewTest(KanisaViewTestCase):
    url = reverse_lazy('kanisa_xhr_biblepassage_check')

    def test_gets_disallowed(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 400)

    def test_must_provide_passage(self):
        resp = self.client.post(self.url, {'foo': 'bar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Passage not found.')

    def test_invalid_passage(self):
        resp = self.client.post(self.url, {'passage': 'Foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         '"Foobar" is not a valid Bible passage.')

    def test_valid_book_invalid_range(self):
        resp = self.client.post(self.url, {'passage': 'Ps 151'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'There are only 150 chapters in Psalms.')

    def test_valid_passage(self):
        resp = self.client.post(self.url, {'passage': 'Matt 3v1-7'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Matthew 3:1-7')


class UserPermissionViewTest(KanisaViewTestCase):
    url = reverse_lazy('kanisa_management_assign_permission')

    def test_must_be_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_gets_disallowed(self):
        self.client.login(username='fred', password='secret')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Permission ID not found.')
        self.client.logout()

    def test_must_provide_required_inputs(self):
        self.client.login(username='fred', password='secret')

        # No permission
        resp = self.client.post(self.url,
                                {'user': '3',
                                 'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Permission ID not found.')

        # No user
        resp = self.client.post(self.url,
                                {'permission': 'foo',
                                 'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'User ID not found.')

        # No 'assigned'
        resp = self.client.post(self.url,
                                {'permission': 'foo',
                                 'user': '3'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Assigned status not found.')

        self.client.logout()

    def test_input_parsing(self):
        self.client.login(username='fred', password='secret')

        resp = self.client.post(self.url,
                                {'permission': 'kanisa.manage_users',
                                 'user': 2,
                                 'assigned': 'true'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         'fred can manage your users.')

        resp = self.client.post(self.url,
                                {'permission': 'kanisa.manage_users',
                                 'user': 2,
                                 'assigned': 'foobar'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         'fred can no longer manage your users.')

        self.client.logout()

    def test_bad_user(self):
        self.client.login(username='fred', password='secret')

        resp = self.client.post(self.url,
                                {'permission': 'kanisa.manage_users',
                                 'user': 99,
                                 'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'No user found with ID 99.')

        self.client.logout()

    def test_bad_permission(self):
        self.client.login(username='fred', password='secret')

        resp = self.client.post(self.url,
                                {'permission': 'kanisa',
                                 'user': 2,
                                 'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Malformed permission: \'kanisa\'.')

        resp = self.client.post(self.url,
                                {'permission': 'kanisa.foo.bar',
                                 'user': 2,
                                 'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'Malformed permission: \'kanisa.foo.bar\'.')

        resp = self.client.post(self.url,
                                {'permission': 'kanisa.raspberries',
                                 'user': 2,
                                 'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'Permission \'kanisa.raspberries\' not found.')

        self.client.logout()
