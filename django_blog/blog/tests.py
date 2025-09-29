# blog/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="password123")
        self.other = User.objects.create_user(username="other", password="password123")
        self.post = Post.objects.create(title="Test Post", content="Content", author=self.user)

    def test_post_list_view(self):
        resp = self.client.get(reverse("blog:post-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test Post")

    def test_create_requires_login(self):
        resp = self.client.get(reverse("blog:post-create"))
        # redirect to login
        self.assertEqual(resp.status_code, 302)

        self.client.login(username="author", password="password123")
        resp = self.client.get(reverse("blog:post-create"))
        self.assertEqual(resp.status_code, 200)

    def test_update_only_author(self):
        self.client.login(username="other", password="password123")
        resp = self.client.get(reverse("blog:post-update", kwargs={"pk": self.post.pk}))
        # other user should be forbidden (redirect or 403 depending), class-based mixin defaults to 403
        self.assertIn(resp.status_code, (302, 403))

        self.client.login(username="author", password="password123")
        resp = self.client.get(reverse("blog:post-update", kwargs={"pk": self.post.pk}))
        self.assertEqual(resp.status_code, 200)
