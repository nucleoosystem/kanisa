from django.core.exceptions import ValidationError
from django.test import TestCase
from kanisa.models import Page
import factory


class PageFactory(factory.Factory):
    FACTORY_FOR = Page
    title = 'Page Title'


class PageTest(TestCase):
    def test_make_non_leaf_node_a_draft(self):
        parent = PageFactory.create()
        child = PageFactory.create(parent=parent)
        p = Page.objects.get(pk=parent.pk)
        p.draft = True

        with self.assertRaises(ValidationError) as cm:
            p.full_clean()

        errors = cm.exception.message_dict
        self.assertTrue('draft' in errors)
        self.assertEqual(errors['draft'],
                         ['Cannot mark this page as draft, as it has '
                          'published descendants.', ])

    def test_make_leaf_node_a_draft(self):
        leaf = PageFactory.create()
        leaf.draft = True
        leaf.full_clean()

    def test_publish_child_of_draft_node(self):
        parent = PageFactory.create(draft=True)
        child = PageFactory.build(parent=parent, draft=False)

        with self.assertRaises(ValidationError) as cm:
            child.full_clean()

        errors = cm.exception.message_dict
        self.assertTrue('draft' in errors)
        self.assertEqual(errors['draft'],
                         ['Cannot mark this page as published, as it '
                          'has non-published ancestors.', ])

    def test_page_cannot_be_its_own_parent(self):
        p = PageFactory.create()
        p.parent = p

        with self.assertRaises(ValidationError) as cm:
            p.full_clean()

        errors = cm.exception.message_dict
        self.assertTrue('parent' in errors)
        self.assertEqual(errors['parent'],
                         ['A page cannot be its own parent.', ])

    def test_page_cannot_have_descendant_as_parent(self):
        parent = PageFactory.create()
        child = PageFactory.create(parent=parent)

        parent.parent = child

        with self.assertRaises(ValidationError) as cm:
            parent.full_clean()

        errors = cm.exception.message_dict
        self.assertTrue('parent' in errors)
        self.assertEqual(errors['parent'],
                         ['Invalid parent - cyclical hierarchy '
                          'detected.', ])
