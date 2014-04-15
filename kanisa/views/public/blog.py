from django.views.generic import DetailView, ListView
from kanisa.models import BlogPost


class BlogIndexView(ListView):
    template_name = 'kanisa/public/blog/index.html'
    queryset = BlogPost.published_objects.all()


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'kanisa/public/blog/post.html'
