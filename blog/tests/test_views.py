from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post


class TestBlogViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        author = User.objects.create(username='sample_author')

        posts = [
            ('post1', 'text1', '2018-09-01 00:00+00:00'),
            ('post2', 'text2', '2018-09-03 00:00+00:00'),
            ('post3', 'text3', '2018-09-05 00:00+00:00'),
            ('post4', 'text4', '2018-09-06 00:00+00:00'),
        ]

        for title, text, published_date in posts:
            Post.objects.create(author=author, title=title, text=text, published_date=published_date)

    def test_posts_list_view(self):
        posts_list_url = reverse('post_list')
        response = self.client.get(posts_list_url)
        self.assertContains(response, 'text4')
        self.assertContains(response, 'text3')
        self.assertContains(response, 'text2')
        self.assertNotContains(response, 'text1')
