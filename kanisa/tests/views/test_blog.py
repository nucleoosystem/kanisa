from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.core.urlresolvers import reverse
from django.http import Http404
from kanisa.tests.test_blog import BlogPostFactory
import kanisa.views.public.blog as views
import pytest


@pytest.fixture()
def posts():
    post1 = BlogPostFactory.create()
    post2 = BlogPostFactory.create(
        publish_date=date(2012, 1, 1)
    )
    post3 = BlogPostFactory.create(
        publish_date=date(date.today().year + 1, 1, 1),
        title="Future post"
    )
    return post1, post2, post3


@pytest.fixture()
def staff_user():
    user = get_user_model().objects.create_user('bob', '', 'secret')
    user.email = 'bob@example.com'
    user.is_staff = False

    user.user_permissions.add(
        Permission.objects.get(codename='manage_blog')
    )

    user.save()
    return user


@pytest.mark.django_db
def test_blog_index(rf, posts):
    post1, post2, post3 = posts
    request = rf.get(reverse('kanisa_public_blog_index'))
    request.user = AnonymousUser()
    response = views.blog_index(request)
    content = response.rendered_content
    assert len(content) > 0
    assert response.status_code == 200

    context = response.context_data
    assert context['years'] == [2012, post1.publish_date.year]
    assert len(context['object_list']) == 2
    assert context['object_list'][0] == post1
    assert context['object_list'][1] == post2


def get_year_view(rf, year, user=None):
    request = rf.get(
        reverse(
            'kanisa_public_blog_year',
            args=[year]
        )
    )

    if not user:
        request.user = AnonymousUser()
    else:
        request.user = user

    return views.blog_year(
        request,
        year='%d' % year
    )


@pytest.mark.django_db
def test_blog_year_archive_recent(rf, posts):
    post1, post2, post3 = posts

    response = get_year_view(rf, post1.publish_date.year)
    content = response.rendered_content
    assert len(content) > 0
    assert response.status_code == 200
    context = response.context_data
    assert context['years'] == [2012, post1.publish_date.year]

    assert len(context['object_list']) == 1
    assert context['object_list'][0] == post1


@pytest.mark.django_db
def test_blog_year_archive_empty(rf):
    with pytest.raises(Http404):
        get_year_view(rf, 2013)


@pytest.mark.django_db
def test_blog_year_archive_future(rf, posts, staff_user):
    post1, _, future_post = posts

    with pytest.raises(Http404):
        get_year_view(rf, future_post.publish_date.year)

    response = get_year_view(
        rf,
        future_post.publish_date.year,
        staff_user
    )

    content = response.rendered_content
    assert len(content) > 0
    assert response.status_code == 200
    context = response.context_data

    assert len(context['object_list']) == 1
    assert context['object_list'][0] == future_post
    assert context['years'] == [
        2012,
        post1.publish_date.year,
        future_post.publish_date.year
    ]


@pytest.mark.django_db
def test_blog_year_archive_old(rf, posts):
    post1, post2, post3 = posts

    response = get_year_view(rf, 2012)
    content = response.rendered_content
    assert len(content) > 0
    context = response.context_data
    assert context['years'] == [2012, post1.publish_date.year]

    assert len(context['object_list']) == 1
    assert context['object_list'][0] == post2

    with pytest.raises(Http404):
        get_year_view(rf, post3.publish_date.year)


def get_blog_detail(rf, post, user=None):
    request = rf.get(post.get_absolute_url())

    if user:
        request.user = user
    else:
        request.user = AnonymousUser()

    return views.blog_detail(
        request,
        year='%d' % post.publish_date.year,
        slug=post.slug
    )


@pytest.mark.django_db
def test_blog_detail_no_next(rf, posts):
    post1, post2, post3 = posts

    response = get_blog_detail(rf, post1)
    assert response.status_code == 200
    content = response.rendered_content
    assert len(content) > 0
    context = response.context_data
    assert context['object'] == post1
    assert context['next'] is None
    assert context['previous'] == post2
    assert context['years'] == [
        2012,
        post1.publish_date.year
    ]


@pytest.mark.django_db
def test_blog_detail_no_previous(rf, posts):
    post1, post2, post3 = posts

    response = get_blog_detail(rf, post2)
    assert response.status_code == 200
    content = response.rendered_content
    assert len(content) > 0
    context = response.context_data
    assert context['object'] == post2
    assert context['next'] == post1
    assert context['previous'] is None
    assert context['years'] == [
        2012,
        post1.publish_date.year
    ]


@pytest.mark.django_db
def test_blog_detail_future(rf, posts, staff_user):
    post1, post2, post3 = posts

    with pytest.raises(Http404):
        get_blog_detail(rf, post3)

    response = get_blog_detail(rf, post3, staff_user)
    assert response.status_code == 200
    content = response.rendered_content
    assert len(content) > 0
    context = response.context_data
    assert context['object'] == post3
    assert context['next'] is None
    assert context['previous'] == post1
    assert context['years'] == [
        2012,
        post1.publish_date.year,
        post3.publish_date.year
    ]
