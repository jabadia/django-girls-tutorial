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
            ('post1', 'text1'),
            ('post2', 'text2'),
            ('post3', 'text3'),
            ('post4', 'text4'),
        ]

        for title, text in posts:
            Post.objects.create(author=author, title=title, text=text)

    def test_posts_list_view(self):
        posts_list_url = reverse('post_list')
        response = self.client.get(posts_list_url)
        self.assertContains(response, 'text1')
        self.assertContains(response, 'text2')
        self.assertContains(response, 'text3')
        self.assertNotContains(response, 'text4')
