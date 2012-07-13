from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class XHRViewTest(KanisaViewTestCase):
    def test_bible_passage_view(self):
        url = reverse('kanisa_xhr_biblepassage_check')
        # No GETs
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post(url, {'foo': 'bar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Passage not found.')

        resp = self.client.post(url, {'passage': 'Foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         '"Foobar" is not a valid Bible passage.')

        resp = self.client.post(url, {'passage': 'Ps 151'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'There are only 150 chapters in Psalms.')

        resp = self.client.post(url, {'passage': 'Matt 3v1-7'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Matthew 3:1-7')
