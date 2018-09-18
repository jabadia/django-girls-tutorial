from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post


class TestBlogModels(TestCase):
    author = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.author = User.objects.create(username='sample_author')

    def test_publish_blog_model(self):
        # initially no posts
        blog_posts = list(Post.objects.filter(title='title'))
        self.assertListEqual(blog_posts, [])

        # we create one post
        blog_post = Post.objects.create(author=self.author, title='title', text='text')

        # we ensure the post is there
        blog_posts = list(Post.objects.filter(title='title'))
        self.assertEqual(len(blog_posts), 1)

        # it's not published yet
        self.assertIsNone(blog_post.published_date)

        # now we publish
        blog_post.publish()
        self.assertIsNotNone(blog_post.published_date)


class TestBlogModelManager(TestCase):
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

    def test_recent_posts(self):
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 4)
        recent_posts = Post.objects.recent_posts(2)
        self.assertEqual(len(recent_posts), 2)
