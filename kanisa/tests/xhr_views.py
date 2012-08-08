from django.core.urlresolvers import reverse_lazy
from kanisa.tests.utils import KanisaViewTestCase


class XHRBaseTestCase(KanisaViewTestCase):
    def fetch(self, params={}):
        if self.method == 'get':
            return self.client.get(self.url, params,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        if self.method == 'post':
            return self.client.post(self.url, params,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_xhr_only(self):
        if self.method == 'get':
            resp = self.client.get(self.url)
        elif self.method == 'post':
            resp = self.client.post(self.url)
        else:
            raise Exception("Invalid XHR method '%s'." % self.method)

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content,
                         'This page is not directly accessible.')

    def test_correct_method_only(self):
        if self.method == 'get':
            resp = self.client.post(self.url)
        elif self.method == 'post':
            resp = self.client.get(self.url)
        else:
            raise Exception("Invalid XHR method '%s'." % self.method)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.content,
                         '')


class XHRBiblePassageViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_xhr_biblepassage_check')
    method = 'post'

    def test_must_provide_passage(self):
        resp = self.fetch({'foo': 'bar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Passage not found.')

    def test_invalid_passage(self):
        resp = self.fetch({'passage': 'Foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         '"Foobar" is not a valid Bible passage.')

    def test_valid_book_invalid_range(self):
        resp = self.fetch({'passage': 'Ps 151'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'There are only 150 chapters in Psalms.')

    def test_valid_passage(self):
        resp = self.fetch({'passage': 'Matt 3v1-7'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Matthew 3:1-7')


class XHRUserPermissionViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_assign_permission')
    method = 'post'

    def test_must_be_authenticated(self):
        resp = self.fetch()
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, ('You do not have permission to '
                                        'manage users.'))

    def test_must_provide_required_inputs(self):
        self.client.login(username='fred', password='secret')

        # No permission
        resp = self.fetch({'user': '3',
                           'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Permission ID not found.')

        # No user
        resp = self.fetch({'permission': 'foo',
                           'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'User ID not found.')

        # No 'assigned'
        resp = self.fetch({'permission': 'foo',
                           'user': '3'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Assigned status not found.')

        self.client.logout()

    def test_input_parsing(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'permission': 'kanisa.manage_users',
                           'user': 2,
                           'assigned': 'true'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         'fred can manage your users.')

        resp = self.fetch({'permission': 'kanisa.manage_users',
                           'user': 2,
                           'assigned': 'foobar'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         'fred can no longer manage your users.')

        self.client.logout()

    def test_bad_user(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'permission': 'kanisa.manage_users',
                           'user': 99,
                           'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'No user found with ID 99.')

        self.client.logout()

    def test_bad_permission(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'permission': 'kanisa',
                           'user': 2,
                           'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Malformed permission: \'kanisa\'.')

        resp = self.fetch({'permission': 'kanisa.foo.bar',
                           'user': 2,
                           'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'Malformed permission: \'kanisa.foo.bar\'.')

        resp = self.fetch({'permission': 'kanisa.raspberries',
                           'user': 2,
                           'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'Permission \'kanisa.raspberries\' not found.')

        self.client.logout()


class XHRCreatePageViewTest(XHRBaseTestCase):
    fixtures = ['pages.json', ]

    url = reverse_lazy('kanisa_manage_xhr_create_page')
    method = 'post'

    def test_must_be_authenticated(self):
        resp = self.fetch()
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, ('You do not have permission to '
                                        'manage pages.'))

    def test_must_provide_required_inputs(self):
        self.client.login(username='fred', password='secret')

        # No title
        resp = self.fetch({'parent': '3', })
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Title not found.')

        # No parent
        resp = self.fetch({'title': 'Test page', })
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Parent not found.')
        self.client.logout()

    def test_empty_title(self):
        self.client.login(username='fred', password='secret')

        # Empty title
        resp = self.fetch({'title': '', 'parent': ''})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Title must not be empty.')
        self.client.logout()

    def test_nonexistent_parent(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'title': 'Test page', 'parent': '99'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Page with ID \'99\' not found.')
        self.client.logout()

    def test_empty_parent(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'title': 'Test page', 'parent': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Page created.')
        self.client.logout()

    def test_good_parent(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'title': 'Test page', 'parent': '1'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Page created.')
        self.client.logout()


class XHRListPagesViewTest(XHRBaseTestCase):
    fixtures = ['pages.json', ]

    url = reverse_lazy('kanisa_manage_xhr_list_pages')
    method = 'get'

    def test_must_be_authenticated(self):
        resp = self.fetch()
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, ('You do not have permission to '
                                        'manage pages.'))

    def test_success(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch()
        self.assertEqual(resp.status_code, 200)
        self.client.logout()


class XHRMarkSermonSeriesComplete(XHRBaseTestCase):
    fixtures = ['sermons.json', ]

    url = reverse_lazy('kanisa_manage_xhr_sermon_series_complete')
    method = 'post'

    def test_must_be_authenticated(self):
        resp = self.fetch()
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, ('You do not have permission to '
                                        'manage sermons.'))

    def test_fails_without_required_parameters(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Series ID not found.')
        self.client.logout()

    def test_fails_with_non_numeric_series(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'series': 'nonnumeric'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "No sermon series found with ID 'nonnumeric'.")
        self.client.logout()

    def test_fails_with_non_existent_series(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'series': 99})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, "No sermon series found with ID '99'.")
        self.client.logout()

    def test_success(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'series': 1})
        self.assertEqual(resp.status_code, 200)
        self.client.logout()


class XHRScheduleRegularEventViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_diary_schedule_regular')
    method = 'post'

    def test_must_be_authenticated(self):
        resp = self.fetch()
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, ('You do not have permission to '
                                        'manage the diary.'))


class XHRFetchScheduleViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_diary_get_schedule',
                       args=['20120101', ])
    method = 'get'

    def test_must_be_authenticated(self):
        resp = self.fetch()
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, ('You do not have permission to '
                                        'manage the diary.'))
