from datetime import date, timedelta
from kanisa.models import BlogPost
import factory
import pytest


class BlogPostFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Title #%d' % n)
    teaser_text = 'Teaser contents'
    main_text = 'Main post contents'
    publish_date = date.today() - timedelta(days=1)

    class Meta:
        model = BlogPost


@pytest.mark.django_db
def test_is_published():
    post = BlogPostFactory.build()
    assert post.published()

    post.publish_date = date.today()
    assert post.published()

    post.publish_date = date.today() + timedelta(days=1)
    assert not post.published()


@pytest.mark.django_db
def test_unicode():
    post = BlogPostFactory.build(
        title='This parrot is dead'
    )
    assert unicode(post) == 'This parrot is dead'


@pytest.mark.django_db
def test_comments_enabled():
    post = BlogPostFactory.build(
        title='This parrot is dead'
    )
    assert post.comments_allowed()

    post.enable_comments = False
    assert not post.comments_allowed()

    post.enable_comments = True
    assert post.comments_allowed()

    post.publish_date = date.today() + timedelta(days=1)
    assert not post.comments_allowed()

    post.publish_date = date.today() + timedelta(days=-15)
    assert post.comments_allowed()

    post.publish_date = date.today() + timedelta(days=-31)
    assert not post.comments_allowed()


@pytest.mark.django_db
def test_slug_uniqueness():
    publish_date = date.today() - timedelta(days=1)
    teaser_text = 'Teaser contents'
    main_text = 'Main post contents'

    post = BlogPost.objects.create(
        title='Slug Generation',
        teaser_text=teaser_text,
        main_text=main_text,
        publish_date=publish_date
    )
    assert post.slug == 'slug-generation'

    # Slugs should not change
    post.title = 'Updated slug'
    post.save()
    post = BlogPost.objects.get(pk=post.pk)
    assert post.slug == 'slug-generation'

    # Slugs should be unique
    post2 = BlogPost.objects.create(
        title='Slug Generation',
        teaser_text=teaser_text,
        main_text=main_text,
        publish_date=publish_date
    )
    assert post2.slug == 'slug-generation-2'

    # Slugs should really be unique
    post3 = BlogPost.objects.create(
        title='Slug Generation',
        teaser_text=teaser_text,
        main_text=main_text,
        publish_date=publish_date
    )
    assert post3.slug == 'slug-generation-3'

    # Slugs should definitely be unique
    post4 = BlogPost.objects.create(
        title='Updated slug',
        teaser_text=teaser_text,
        main_text=main_text,
        publish_date=publish_date
    )
    assert post4.slug == 'updated-slug'


@pytest.mark.django_db
def test_slug_uniqueness():
    publish_date = date.today() - timedelta(days=1)
    teaser_text = 'Teaser contents'
    main_text = 'Main post contents'

    slug_base = 'This is my really great slug it is around 50 bytes'
    assert len(slug_base) == 50

    post = BlogPost.objects.create(
        title=slug_base + " (first)",
        teaser_text=teaser_text,
        main_text=main_text,
        publish_date=publish_date
    )
    assert post.slug == 'this-is-my-really-great-slug-it-is-around-50-bytes'

    post2 = BlogPost.objects.create(
        title=slug_base + " (second)",
        teaser_text=teaser_text,
        main_text=main_text,
        publish_date=publish_date
    )
    assert post2.slug == 'this-is-my-really-great-slug-it-is-around-50-byt-2'
