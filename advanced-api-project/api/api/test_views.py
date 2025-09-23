from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book


class BookAPITests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client = APIClient()
        self.client.login(username="testuser", password="testpass123")

        # Sample book
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            publication_year=2020
        )

        self.list_url = reverse("book-list")   # maps to BookListView
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book.pk})

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    def test_create_book(self):
        data = {"title": "New Book", "author": "Jane Doe", "publication_year": 2021}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        data = {"title": "Updated Title", "author": "John Doe", "publication_year": 2020}
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {"author": "John Doe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    def test_search_books(self):
        response = self.client.get(self.list_url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    def test_order_books_by_year(self):
        Book.objects.create(title="Older Book", author="Jane Doe", publication_year=1999)
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]["publication_year"] <= response.data[1]["publication_year"])
