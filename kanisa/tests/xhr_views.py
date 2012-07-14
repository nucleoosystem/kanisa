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
