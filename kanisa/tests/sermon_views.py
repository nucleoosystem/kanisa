from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class SermonManagementViewTest(KanisaViewTestCase):
    def test_views_protected(self):
        prefix = 'kanisa_manage_sermons'
        self.check_staff_only_302(reverse(prefix))
        self.check_staff_only_302(reverse('%s_series_create' % prefix))
        self.check_staff_only_302(reverse('%s_individual_create' % prefix))
        self.check_staff_only_302(reverse('%s_speaker' % prefix))
        self.check_staff_only_302(reverse('%s_speaker_create' % prefix))

        # These would 404 if you were logged in
        self.check_staff_only_302(reverse('%s_series_detail' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_series_update' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_series_complete' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_individual_update' % prefix,
                                          args=[1, ]))
        self.check_staff_only_302(reverse('%s_speaker_update' % prefix,
                                          args=[1, ]))
