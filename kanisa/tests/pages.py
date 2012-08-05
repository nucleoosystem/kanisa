from django.core.exceptions import ValidationError
from django.test import TestCase
from kanisa.models import Page


class PageTest(TestCase):
    fixtures = ['pages.json', ]

    def test_make_non_leaf_node_a_draft(self):
        p = Page.objects.get(pk=1)
        p.draft = True
        try:
            p.full_clean()
            # Shouldn't get here
            self.assertFalse(True)
        except ValidationError, e:
            errors = e.message_dict
            self.assertTrue('draft' in errors)
            self.assertEqual(errors['draft'],
                             ['Cannot mark this page as draft, as it has '
                              'published descendants.', ])

    def test_make_leaf_node_a_draft(self):
        p = Page.objects.get(pk=4)
        self.assertTrue(p.is_leaf_node())
        p.draft = True
        p.full_clean()

    def test_publish_child_of_draft_node(self):
        p = Page.objects.get(pk=4)
        p.draft = True
        p.save()

        new_page = Page.objects.create(title='Child of draft node',
                                       parent=p)
        new_page.save()
        new_page.draft = False

        try:
            new_page.full_clean()
            # Shouldn't get here
            self.assertFalse(True)
        except ValidationError, e:
            errors = e.message_dict
            self.assertTrue('draft' in errors)
            self.assertEqual(errors['draft'],
                             ['Cannot mark this page as published, as it '
                              'has non-published ancestors.', ])

    def test_page_cannot_be_its_own_parent(self):
        p = Page.objects.get(pk=4)
        p.parent = p

        try:
            p.full_clean()
            # Shouldn't get here
            self.assertFalse(True)
        except ValidationError, e:
            errors = e.message_dict
            self.assertTrue('parent' in errors)
            self.assertEqual(errors['parent'],
                             ['A page cannot be its own parent.', ])

    def test_page_cannot_have_descendant_as_parent(self):
        p = Page.objects.get(pk=1)
        descendants = p.get_descendants()
        self.assertEqual([d.pk for d in descendants],
                         [4, 3, 2, ])

        p.parent = Page.objects.get(pk=4)

        try:
            p.full_clean()
            # Shouldn't get here
            self.assertFalse(True)
        except ValidationError, e:
            errors = e.message_dict
            self.assertTrue('parent' in errors)
            self.assertEqual(errors['parent'],
                             ['Invalid parent - cyclical hierarchy '
                              'detected.', ])
