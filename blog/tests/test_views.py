from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post


class BlogTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        author = User.objects.create_user(username='sample_author', password='123456')
        author.save()

        posts = [
            ('post1', 'text1', '2018-09-01 00:00+00:00'),
            ('post2', 'text2', '2018-09-03 00:00+00:00'),
            ('post3', 'text3', '2018-09-05 00:00+00:00'),
            ('post4', 'text4', '2018-09-06 00:00+00:00'),
        ]

        for title, text, published_date in posts:
            post = Post(author=author, title=title, text=text, published_date=published_date)
            post.save()


class TestBlogViews(BlogTestCase):
    
    def test_not_authenticated_view(self):
        posts_list_url = reverse('post_list')
        response = self.client.get(posts_list_url)
        self.assertContains(
            response,
            '<span class="username"><a href="/admin/login/?next=/">login</a> to add a new post</span>',
            html=True
        )
        self.assertNotContains(response, '<span class="glyphicon glyphicon-plus"></span>', html=True)
        self.assertNotContains(response, '<a href="/post/new/"')

    def test_authenticated_view(self):
        user_login = self.client.login(username='sample_author', password='123456')
        self.assertTrue(user_login)
        posts_list_url = reverse('post_list')
        response = self.client.get(posts_list_url)
        self.assertContains(
            response,
            '<span class="username">Hola sample_author! <a href="/admin/logout/?next=/">(logout)</a></span>',
            html=True
        )
        self.assertContains(
            response,
            '<a href="/post/new/" class="top-menu"><span class="glyphicon glyphicon-plus"></span></a>',
            html=True
        )

    def test_posts_list_view(self):
        posts_list_url = reverse('post_list')
        response = self.client.get(posts_list_url)
        self.assertContains(response, 'text4')
        self.assertContains(response, 'text3')
        self.assertContains(response, 'text2')
        self.assertNotContains(response, 'text1')

    def test_post_detail_view(self):
        post_detail_url = reverse('post_detail', kwargs={'pk': 1})
        response = self.client.get(post_detail_url)
        self.assertContains(response, '1 de Septiembre de 2018 a las 02:00')
        self.assertContains(response, '<h1>post1</h1>', html=True)
        self.assertContains(response, '<p>text1</p>', html=True)

    def test_post_new_view(self):
        user_login = self.client.login(username='sample_author', password='123456')
        self.assertTrue(user_login)
        new_post_url = reverse('post_new')
        response = self.client.get(new_post_url)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        new_post_data = {
            'title': 'new post title',
            'text': 'new post text',
        }
        response = self.client.post(new_post_url, new_post_data, follow=True)
        new_post_detail_url = reverse('post_detail', kwargs={'pk': 5})
        self.assertRedirects(response, new_post_detail_url, status_code=302, target_status_code=200)
        self.assertContains(response, '<h1>%s</h1>' % (new_post_data['title'],), html=True)
        self.assertContains(response, '<p>%s</p>' % (new_post_data['text'],), html=True)
