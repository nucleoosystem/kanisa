from datetime import date
from django.core.urlresolvers import reverse_lazy

from kanisa.forms.blog import BlogPostForm
from kanisa.models import BlogPost
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaCreateView,
    KanisaUpdateView,
    KanisaListView
)


class BlogBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Blog posts give you a place to publish news, views and '
                   'updates.')
    kanisa_root_crumb = {'text': 'Blog',
                         'url': reverse_lazy('kanisa_manage_blog')}
    permission = 'kanisa.manage_blog'
    kanisa_nav_component = 'blog'


class BlogManagementView(BlogBaseView,
                         KanisaListView):
    model = BlogPost
    template_name = 'kanisa/management/blog/index.html'
    kanisa_title = 'Manage the Blog'
    kanisa_is_root_view = True
blog_management = BlogManagementView.as_view()


class BlogCreateView(BlogBaseView,
                     KanisaCreateView):
    model = BlogPost
    form_class = BlogPostForm
    kanisa_title = 'Write a Blog Post'
    success_url = reverse_lazy('kanisa_manage_blog')

    def get_form(self):
        form = super(BlogCreateView, self).get_form()
        form.initial = {
            'author': self.request.user,
            'publish_date': date.today()
        }
        return form
blog_create = BlogCreateView.as_view()


class BlogUpdateView(BlogBaseView,
                     KanisaUpdateView):
    model = BlogPost
    form_class = BlogPostForm
    success_url = reverse_lazy('kanisa_manage_blog')

blog_update = BlogUpdateView.as_view()
