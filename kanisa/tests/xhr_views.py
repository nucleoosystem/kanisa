from django.core.urlresolvers import reverse, reverse_lazy
from datetime import time
from django.test.client import RequestFactory
from kanisa.models import ScheduledEvent, Page, SermonSeries, RegularEvent
from kanisa.tests.utils import KanisaViewTestCase
from kanisa.views.xhr.users import AssignPermissionView

import factory


class XHRBaseTestCase(KanisaViewTestCase):
    def setUp(self):
        super(XHRBaseTestCase, self).setUp()
        factory = RequestFactory()

        if self.method == 'post':
            self.request = factory.post(self.url)
        else:
            self.request = factory.get(self.url)

        self.request.session = {}
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

    def fetch_url(self, url, params={}):
        if self.method == 'get':
            return self.client.get(url, params,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        if self.method == 'post':
            return self.client.post(url, params,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def fetch(self, params={}):
        return self.fetch_url(self.url, params)

    def test_xhr_only(self):
        if self.method == 'get':
            resp = self.client.get(self.url)
        elif self.method == 'post':
            resp = self.client.post(self.url)

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content,
                         'This page is not directly accessible.')

    def test_correct_method_only(self):
        if self.method == 'get':
            resp = self.client.post(self.url)
        elif self.method == 'post':
            resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.content,
                         '')

    def test_must_be_authenticated(self):
        if not hasattr(self, 'permission_text'):
            return

        resp = self.fetch()
        self.assertEqual(resp.status_code, 403)

    def fetch_from_factory(self, params):
        if self.method == 'post':
            self.request.POST = params
        elif self.method == 'get':
            self.request.GET = params

        return self.view.as_view()(self.request)


class XHRBiblePassageViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_xhr_biblepassage_check')
    method = 'post'

    def test_must_provide_passage(self):
        resp = self.fetch({'foo': 'bar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'passage' not found.")

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
    permission_text = 'manage users'
    view = AssignPermissionView

    def test_must_provide_required_inputs(self):
        self.request.user = self.fred

        # No permission
        resp = self.fetch_from_factory({'user': '3',
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'permission' not found.")

        # No user
        resp = self.fetch_from_factory({'permission': 'foo',
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'user' not found.")

        # No 'assigned'
        resp = self.fetch_from_factory({'permission': 'foo',
                                        'user': '3'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'assigned' not found.")

    def test_input_parsing(self):
        self.request.user = self.fred

        resp = self.fetch_from_factory({'permission': 'kanisa.manage_users',
                                        'user': 2,
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         'fred can manage your users.')

        resp = self.fetch_from_factory({'permission': 'kanisa.manage_users',
                                        'user': 2,
                                        'assigned': 'foobar'})
        resp = self.view.as_view()(self.request)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         'fred can no longer manage your users.')

    def test_bad_user(self):
        self.request.user = self.fred

        resp = self.fetch_from_factory({'permission': 'kanisa.manage_users',
                                        'user': 99,
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'No user found with ID 99.')

    def test_bad_permission(self):
        self.request.user = self.fred

        resp = self.fetch_from_factory({'permission': 'kanisa',
                                        'user': 2,
                                        'assigned': 'true'})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Malformed permission: \'kanisa\'.')

        resp = self.fetch_from_factory({'permission': 'kanisa.foo.bar',
                                        'user': 2,
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'Malformed permission: \'kanisa.foo.bar\'.')

        resp = self.fetch_from_factory({'permission': 'kanisa.raspberries',
                                        'user': 2,
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'Permission \'kanisa.raspberries\' not found.')


class PageFactory(factory.Factory):
    FACTORY_FOR = Page
    title = 'Page Title'


class XHRCreatePageViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_create_page')
    method = 'post'
    permission_text = 'manage pages'

    def test_must_provide_required_inputs(self):
        self.client.login(username='fred', password='secret')

        # No title
        resp = self.fetch({'parent': '3', })
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'title' not found.")

        # No parent
        resp = self.fetch({'title': 'Test page', })
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'parent' not found.")
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
        pk = PageFactory.create().pk
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'title': 'Test page', 'parent': '%s' % pk})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Page created.')
        self.client.logout()


class XHRListPagesViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_list_pages')
    method = 'get'
    permission_text = 'manage pages'

    def test_success(self):
        # Make some sample data
        parent = PageFactory.create()
        PageFactory.create(parent=parent)
        PageFactory.create()

        self.client.login(username='fred', password='secret')

        resp = self.fetch()
        self.assertEqual(resp.status_code, 200)
        self.client.logout()


class SermonSeriesFactory(factory.Factory):
    FACTORY_FOR = SermonSeries
    title = factory.Sequence(lambda n: 'Series #%s' % n)


class XHRMarkSermonSeriesComplete(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_sermon_series_complete')
    method = 'post'
    permission_text = 'manage sermons'

    def test_fails_without_required_parameters(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'series' not found.")
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
        pk = SermonSeriesFactory.create().pk

        self.client.login(username='fred', password='secret')

        resp = self.fetch({'series': pk})
        self.assertEqual(resp.status_code, 200)
        self.client.logout()


class RegularEventFactory(factory.Factory):
    FACTORY_FOR = RegularEvent
    title = factory.Sequence(lambda n: 'Regular Event #' + n)
    start_time = time(14, 0)
    duration = 60
    day = 1


class XHRScheduleRegularEventViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_diary_schedule_regular')
    method = 'post'
    permission_text = 'manage the diary'

    def test_required_attributes_are_required(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'date': 'foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'event' not found.")

        resp = self.fetch({'event': 'foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'date' not found.")

        self.client.logout()

    def test_bad_date_format(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'event': 'foobar',
                           'date': '20121301'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, "'20121301' is not a valid date.")

        self.client.logout()

    def test_bad_event_id(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'event': '99',
                           'date': '20121201'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, "No event found with ID '99'.")

        self.client.logout()

    def test_success(self):
        pk = RegularEventFactory.create().pk
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'event': '%s' % pk,
                           'date': '20120103'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, "Event scheduled.")

        events = ScheduledEvent.objects.filter(event__pk=1,
                                               date='2012-01-03')
        self.assertEqual(len(events), 1)

        self.client.logout()

    def test_double_schedule(self):
        pk = RegularEventFactory.create().pk
        self.client.login(username='fred', password='secret')

        resp = self.fetch({'event': '%s' % pk,
                           'date': '20120110'})
        self.assertEqual(resp.status_code, 200)

        resp = self.fetch({'event': '%s' % pk,
                           'date': '20120110'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'That event is already scheduled.')
        self.client.logout()


class XHRFetchScheduleViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_diary_get_schedule',
                       args=['20120101', ])
    method = 'get'
    permission_text = 'manage the diary'

    def test_success(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch()
        self.assertEqual(resp.status_code, 200)
        self.client.logout()

    def test_baddate(self):
        self.client.login(username='fred', password='secret')

        resp = self.fetch_url(reverse('kanisa_manage_xhr_diary_get_schedule',
                                      args=[2012, ]))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, "Invalid date '2012' provided.")
        self.client.logout()
