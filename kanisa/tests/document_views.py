from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class DocumentManagementViewTest(KanisaViewTestCase):
    def test_views_protected(self):
        self.view_is_restricted(reverse('kanisa_manage_documents'))
        self.view_is_restricted(reverse('kanisa_manage_documents_create'))
        self.view_is_restricted(reverse('kanisa_manage_documents_search'))

        # These would 404 if you were logged in
        self.view_is_restricted(reverse('kanisa_manage_documents_update',
                                        args=[1, ]))
        self.view_is_restricted(reverse('kanisa_manage_documents_delete',
                                        args=[1, ]))
