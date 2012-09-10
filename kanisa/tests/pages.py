from django.core.exceptions import ValidationError
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from kanisa.models import Page
from kanisa.models.pages import get_page_for_request
import factory


class PageFactory(factory.Factory):
    FACTORY_FOR = Page
    title = 'Page Title'


class PageTest(TestCase):
    def test_make_non_leaf_node_a_draft(self):
        parent = PageFactory.create()
        PageFactory.create(parent=parent)
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
                         ['Cannot mark this page as published, as its '
                          'parent page (Page Title) is currently a draft.', ])

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


class GetPageFromPathTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_raises_http_404_on_empty_request(self):
        with self.assertNumQueries(0):
            request = self.factory.get('')

            with self.assertRaises(Http404):
                get_page_for_request(request)

            request = self.factory.get('/')

            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_root_page(self):
        page = PageFactory.create(title='Hello')
        self.assertEqual(page.slug, 'hello')

        with self.assertNumQueries(1):
            request = self.factory.get('/hello/')
            self.assertEqual(page, get_page_for_request(request))

    def test_root_page_double_slash(self):
        page = PageFactory.create(title='Hello')
        self.assertEqual(page.slug, 'hello')

        request = self.factory.get('/hello//')

        with self.assertNumQueries(1):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_root_page_without_trailing_slash(self):
        page = PageFactory.create(title='Hello')
        self.assertEqual(page.slug, 'hello')

        request = self.factory.get('/hello')

        with self.assertNumQueries(0):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_nonexistent_root_page(self):
        request = self.factory.get('/hello/')

        with self.assertNumQueries(1):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_fetch_unpublished_page_fails(self):
        page = PageFactory.create(title='Hello',
                                  draft=True)
        self.assertEqual(page.slug, 'hello')

        request = self.factory.get('/hello/')

        with self.assertNumQueries(1):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_fetch_child_page_without_path_fails(self):
        root = PageFactory.create(title='root')
        PageFactory.create(title='child', parent=root)

        request = self.factory.get('/child/')

        with self.assertNumQueries(1):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_fetch_child_page(self):
        root = PageFactory.create(title='root')
        child = PageFactory.create(title='child', parent=root)
        child2 = PageFactory.create(title='child2', parent=root)
        grandchild = PageFactory.create(title='grandchild', parent=child)
        PageFactory.create(title='grandchild2', parent=child)
        PageFactory.create(title='grandchild3', parent=child2)

        request = self.factory.get('/root/child/grandchild/')

        with self.assertNumQueries(2):
            self.assertEqual(grandchild, get_page_for_request(request))

    def test_fetch_child_page_without_trailing_slash(self):
        root = PageFactory.create(title='root')
        child = PageFactory.create(title='child', parent=root)
        child2 = PageFactory.create(title='child2', parent=root)
        PageFactory.create(title='grandchild', parent=child)
        PageFactory.create(title='grandchild2', parent=child)
        PageFactory.create(title='grandchild3', parent=child2)

        request = self.factory.get('/root/child/grandchild')

        with self.assertNumQueries(0):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_fetch_child_page_with_repeated_part(self):
        root = PageFactory.create(title='root')
        child = PageFactory.create(title='child', parent=root)
        child2 = PageFactory.create(title='child2', parent=root)
        PageFactory.create(title='grandchild', parent=child)
        PageFactory.create(title='grandchild2', parent=child)
        PageFactory.create(title='grandchild3', parent=child2)

        request = self.factory.get('/root/root/child/grandchild/')

        with self.assertNumQueries(2):
            with self.assertRaises(Http404):
                get_page_for_request(request)

        request = self.factory.get('/root/child/child/grandchild/')

        with self.assertNumQueries(2):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_fetch_path_with_existent_prefix_fails_on_nonexistent_suffix(self):
        root = PageFactory.create(title='root')
        PageFactory.create(title='child', parent=root)

        request = self.factory.get('/root/child/foobar/')

        with self.assertNumQueries(2):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_fetch_path_with_missing_part_halfway_through(self):
        root = PageFactory.create(title='root')
        child = PageFactory.create(title='child', parent=root)
        PageFactory.create(title='grandchild', parent=child)

        request = self.factory.get('/root/foobar/child/')

        with self.assertNumQueries(2):
            with self.assertRaises(Http404):
                get_page_for_request(request)

    def test_fetch_path_with_wrong_parent(self):
        root = PageFactory.create(title='root')
        child = PageFactory.create(title='child', parent=root)
        PageFactory.create(title='grandchild', parent=child)

        request = self.factory.get('/root/grandchild/')

        with self.assertNumQueries(2):
            with self.assertRaises(Http404):
                get_page_for_request(request)
