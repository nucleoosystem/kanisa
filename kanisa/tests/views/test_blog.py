from datetime import date
from django.core.urlresolvers import reverse
from django.http import Http404
from kanisa.tests.test_blog import BlogPostFactory
import kanisa.views.public.blog as views
import pytest


@pytest.mark.django_db
def test_blog_index(rf):
    post1 = BlogPostFactory.create()
    post2 = BlogPostFactory.create(
        publish_date=date(2012, 1, 1)
    )
    BlogPostFactory.create(
        publish_date=date(date.today().year + 1, 1, 1)
    )

    request = rf.get(reverse('kanisa_public_blog_index'))
    response = views.blog_index(request)
    content = response.rendered_content
    assert len(content) > 0
    assert response.status_code == 200

    context = response.context_data
    assert context['years'] == [2012, post1.publish_date.year]
    assert len(context['object_list']) == 2
    assert context['object_list'][0] == post1
    assert context['object_list'][1] == post2


@pytest.mark.django_db
def test_blog_year_archive(rf):
    def get(rf, year):
        request = rf.get(
            reverse(
                'kanisa_public_blog_year',
                args=[year]
            )
        )

        return views.blog_year(
            request,
            year='%d' % year
        )

    post1 = BlogPostFactory.create()
    post2 = BlogPostFactory.create(
        publish_date=date(2012, 1, 1)
    )
    post3 = BlogPostFactory.create(
        publish_date=date(date.today().year + 1, 1, 1)
    )

    response = get(rf, post1.publish_date.year)
    content = response.rendered_content
    assert len(content) > 0
    assert response.status_code == 200
    context = response.context_data
    assert context['years'] == [2012, post1.publish_date.year]

    assert len(context['object_list']) == 1
    assert context['object_list'][0] == post1

    with pytest.raises(Http404):
        get(rf, 2013)

    response = get(rf, 2012)
    content = response.rendered_content
    assert len(content) > 0
    context = response.context_data
    assert context['years'] == [2012, post1.publish_date.year]

    assert len(context['object_list']) == 1
    assert context['object_list'][0] == post2

    with pytest.raises(Http404):
        get(rf, post3.publish_date.year)


@pytest.mark.django_db
def test_blog_detail(rf):
    def get(rf, post):
        request = rf.get(post.get_absolute_url())

        return views.blog_detail(
            request,
            year='%d' % post.publish_date.year,
            slug=post.slug
        )

    post1 = BlogPostFactory.create()
    post2 = BlogPostFactory.create(
        publish_date=date(2012, 1, 1)
    )
    post3 = BlogPostFactory.create(
        publish_date=date(date.today().year + 1, 1, 1),
        title='Future post'
    )

    response = get(rf, post1)
    assert response.status_code == 200
    content = response.rendered_content
    assert len(content) > 0
    context = response.context_data
    assert context['object'] == post1
    assert context['next'] is None
    assert context['previous'] == post2

    response = get(rf, post2)
    assert response.status_code == 200
    content = response.rendered_content
    assert len(content) > 0
    context = response.context_data
    assert context['object'] == post2
    assert context['next'] == post1
    assert context['previous'] is None

    with pytest.raises(Http404):
        get(rf, post3)
