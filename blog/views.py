from django.shortcuts import render

from blog.models import Post


def post_list(request):
    recent_posts = Post.objects.recent_posts(3)
    return render(request, 'blog/post_list.html', {
        'recent_posts': recent_posts
    })
