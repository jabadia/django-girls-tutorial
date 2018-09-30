from django.core.urlresolvers import reverse
from django.test import TestCase

from blog.forms import PostForm
from blog.models import Post
from blog.tests.test_views import BlogTestCase


class TestBlogForm(TestCase):

    def test_empty_form(self):
        form = PostForm(data={'title': '', 'text': ''})
        self.assertFalse(form.is_valid())

    def test_invalid_form1(self):
        form = PostForm(data={
            'title': 'good title',
            'text': ''
        })
        self.assertFalse(form.is_valid())

    def test_invalid_form2(self):
        form = PostForm(data={
            'title': '',
            'text': 'good text'
        })
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        form = PostForm(data={'title': 'post title', 'text': 'post text'})
        self.assertTrue(form.is_valid())


class TestBlogFormViews(BlogTestCase):

    def test_edit_form_view(self):
        user_login = self.client.login(username='sample_author', password='123456')
        self.assertTrue(user_login)
        post_edit_url = reverse('post_edit', kwargs={'pk': 1})
        response = self.client.get(post_edit_url)
        self.assertContains(response, '<h1>New post</h1>', html=True)

    def test_edit_empty_form_view(self):
        post_edit_url = reverse('post_edit', kwargs={'pk': 1})
        empty_form = {
            'title': '',
            'text': '',
        }
        response = self.client.post(post_edit_url, empty_form)

        self.assertFormError(response, 'form', 'title', ['Este campo es obligatorio.'])
        self.assertFormError(response, 'form', 'text', ['Este campo es obligatorio.'])

        unchanged_post = Post.objects.get(pk=1)
        self.assertEqual(unchanged_post.title, 'post1')
        self.assertEqual(unchanged_post.text, 'text1')

    def test_edit_invalid_field_form_view(self):
        post_edit_url = reverse('post_edit', kwargs={'pk': 1})
        invalid_field_form = {
            'title': '',
            'text': 'text_modified',
        }
        response = self.client.post(post_edit_url, invalid_field_form)

        self.assertFormError(response, 'form', 'title', ['Este campo es obligatorio.'])

        unchanged_post = Post.objects.get(pk=1)
        self.assertEqual(unchanged_post.title, 'post1')
        self.assertEqual(unchanged_post.text, 'text1')

    def test_edit_valid_form_view(self):
        user_login = self.client.login(username='sample_author', password='123456')
        self.assertTrue(user_login)
        post_edit_url = reverse('post_edit', kwargs={'pk': 1})
        valid_form = {
            'title': 'post1_changed',
            'text': 'text1_changed',
        }
        response = self.client.post(post_edit_url, valid_form)
        post_detail_url = reverse('post_detail', kwargs={'pk': 1})
        self.assertRedirects(response, post_detail_url, status_code=302, target_status_code=200)

        modified_post = Post.objects.get(pk=1)
        self.assertEqual(modified_post.title, valid_form['title'])
        self.assertEqual(modified_post.text, valid_form['text'])
