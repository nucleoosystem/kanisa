from datetime import date
from django.views.generic import (
    DetailView,
    ListView,
    YearArchiveView,
)
from kanisa.models import BlogPost


class BlogMixin(object):
    def get_base_queryset(self):
        if self.request.user.has_perm('kanisa.manage_blog'):
            return BlogPost.objects.all()

        return BlogPost.published_objects.all()

    def get_queryset(self):
        return self.get_base_queryset()

    def get_context_data(self, **kwargs):
        context = super(BlogMixin, self).get_context_data(**kwargs)
        dates = self.get_base_queryset().dates(
            'publish_date',
            'year'
        )
        context['years'] = [d.year for d in dates]
        return context


class BlogIndexView(BlogMixin, ListView):
    template_name = 'kanisa/public/blog/index.html'
    paginate_by = 10
blog_index = BlogIndexView.as_view()


class BlogYearView(BlogMixin, YearArchiveView):
    template_name = 'kanisa/public/blog/year.html'
    date_field = 'publish_date'
    make_object_list = True
    allow_future = True
blog_year = BlogYearView.as_view()


class BlogPostDetailView(BlogMixin, DetailView):
    queryset = BlogPost.published_objects.all()
    template_name = 'kanisa/public/blog/post.html'

    def get_queryset(self):
        qs = super(BlogPostDetailView, self).get_queryset()
        qs = qs.filter(publish_date__year=self.kwargs['year'])
        return qs

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)

        try:
            next_post = self.object.get_next_by_publish_date()
            if next_post.publish_date > date.today():
                next_post = None
        except BlogPost.DoesNotExist:
            next_post = None

        try:
            previous_post = self.object.get_previous_by_publish_date()
        except BlogPost.DoesNotExist:
            previous_post = None

        context['next'] = next_post
        context['previous'] = previous_post

        return context
blog_detail = BlogPostDetailView.as_view()
