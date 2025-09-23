from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User


class BookAPITests(APITestCase):
    """
    Unit tests for Book API endpoints.
    Verifies CRUD operations, permissions, and query features.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", publication_year=2020, author=self.author
        )
        self.book_list_url = reverse("book-list")
        self.book_detail_url = reverse("book-detail", args=[self.book.id])

    def test_list_books(self):
        """Ensure we can list books (200 OK)."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_unauthenticated(self):
        """Unauthenticated user cannot create book (403 Forbidden)."""
        data = {"title": "New Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Authenticated user can create book (201 Created)."""
        self.client.login(username="testuser", password="testpass")
        data = {"title": "New Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        """Authenticated user can update book (200 OK)."""
        self.client.login(username="testuser", password="testpass")
        data = {"title": "Updated Book", "publication_year": 2022, "author": self.author.id}
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        """Authenticated user can delete book (204 No Content)."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_books(self):
        """Test filtering by title."""
        response = self.client.get(self.book_list_url, {"title": "Test Book"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self):
        """Test searching by title."""
        response = self.client.get(self.book_list_url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_books(self):
        """Test ordering by publication_year."""
        response = self.client.get(self.book_list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
