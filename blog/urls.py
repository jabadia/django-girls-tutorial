from django.conf.urls import include, url

from . import cb_views
from . import views

urlpatterns = [
    url(r'^$', cb_views.PostList.as_view(), name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', cb_views.PostDetail.as_view(), name='post_detail'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', cb_views.PostEdit.as_view(), name='post_edit'),
    url(r'^post/new/$', views.post_new, name='post_new'),
]
