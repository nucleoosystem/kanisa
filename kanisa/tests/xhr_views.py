from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class XHRViewTest(KanisaViewTestCase):
    def test_bible_passage_view_gets_disallowed(self):
        url = reverse('kanisa_xhr_biblepassage_check')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)

    def test_bible_passage_view_must_provide_passage(self):
        url = reverse('kanisa_xhr_biblepassage_check')
        resp = self.client.post(url, {'foo': 'bar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Passage not found.')

    def test_bible_passage_view_invalid_passage(self):
        url = reverse('kanisa_xhr_biblepassage_check')
        resp = self.client.post(url, {'passage': 'Foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         '"Foobar" is not a valid Bible passage.')

    def test_bible_passage_view_valid_book_invalid_range(self):
        url = reverse('kanisa_xhr_biblepassage_check')
        resp = self.client.post(url, {'passage': 'Ps 151'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'There are only 150 chapters in Psalms.')

    def test_bible_passage_view_valid_passage(self):
        url = reverse('kanisa_xhr_biblepassage_check')
        resp = self.client.post(url, {'passage': 'Matt 3v1-7'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Matthew 3:1-7')
