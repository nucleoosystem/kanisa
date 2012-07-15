from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class SocialViewTestCase(KanisaViewTestCase):
    def test_views_protected(self):
        prefix = 'kanisa_manage_social'
        self.check_staff_only_302(reverse(prefix))
        self.check_staff_only_302(reverse('%s_twitter' % prefix))
        self.check_staff_only_302(reverse('%s_twitter_create' % prefix))
        self.check_staff_only_302(reverse('%s_twitter_update' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_twitter_delete' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_twitter_post' % prefix))
