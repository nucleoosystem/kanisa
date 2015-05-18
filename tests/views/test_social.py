from django.core.urlresolvers import reverse
from tests.utils import KanisaViewTestCase


class SocialViewTest(KanisaViewTestCase):
    def test_views_protected(self):
        prefix = 'kanisa_manage_social'
        self.view_is_restricted(reverse(prefix))
        self.view_is_restricted(reverse('%s_twitter' % prefix))
        self.view_is_restricted(reverse('%s_twitter_create' % prefix))
        self.view_is_restricted(reverse('%s_twitter_update' % prefix,
                                        args=[1, ]))
        self.view_is_restricted(reverse('%s_twitter_delete' % prefix,
                                        args=[1, ]))
        self.view_is_restricted(reverse('%s_twitter_post' % prefix))
