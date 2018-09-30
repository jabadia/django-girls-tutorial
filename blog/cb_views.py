from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, UpdateView

from blog.forms import PostForm
from blog.models import Post


class PostList(ListView):
    queryset = Post.objects.recent_posts(3)
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


class PostEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        post = self.get_object()
        return reverse('post_detail', kwargs={'pk': post.pk})
