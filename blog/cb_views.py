from django.views.generic import ListView, DetailView

from blog.models import Post


class PostList(ListView):
    queryset = Post.objects.recent_posts(3)
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'
