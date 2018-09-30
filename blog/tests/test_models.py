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
            ('post1', 'text1', '2018-09-01 00:00+00:00'),
            ('post2', 'text2', '2018-09-03 00:00+00:00'),
            ('post3', 'text3', '2018-09-05 00:00+00:00'),
            ('post4', 'text4', '2018-09-06 00:00+00:00'),
        ]

        for title, text, published_date in posts:
            Post.objects.create(author=author, title=title, text=text, published_date=published_date)

    def test_post_repr(self):
        post = Post.objects.get(pk=1)
        self.assertEqual('<Post: %s>' % (post.title,), repr(post))

    def test_all_posts(self):
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 4)
        all_post_titles = [post.title for post in all_posts]
        self.assertListEqual(all_post_titles, ['post1', 'post2', 'post3', 'post4'])

    def test_recent_posts(self):
        recent_posts = Post.objects.recent_posts(2)
        self.assertEqual(len(recent_posts), 2)
        recent_post_titles = [post.title for post in recent_posts]
        self.assertIn('post3', recent_post_titles)
        self.assertIn('post4', recent_post_titles)
        self.assertNotIn('post1', recent_post_titles)
        self.assertNotIn('post2', recent_post_titles)
