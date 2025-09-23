from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="tester", password="testpass123")

        # Create an author
        self.author = Author.objects.create(name="John Doe")

        # Create a sample book
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2021
        )

        # URLs
        self.book_list_url = reverse("book-list")
        self.book_detail_url = reverse("book-detail", kwargs={"pk": self.book.id})

        # Auth client
        self.client.login(username="tester", password="testpass123")

    def test_list_books(self):
        """Ensure we can list books (200 OK)."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    def test_create_book_authenticated(self):
        """Authenticated user can create book (201 Created)."""
        data = {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2022,
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """Unauthenticated user cannot create book (403 Forbidden)."""
        self.client.logout()
        data = {
            "title": "Blocked Book",
            "author": self.author.id,
            "publication_year": 2023,
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        """Authenticated user can update book (200 OK)."""
        data = {
            "title": "Updated Book",
            "author": self.author.id,
            "publication_year": 2024,
        }
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        """Authenticated user can delete book (204 No Content)."""
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        """Test filtering by title."""
        response = self.client.get(self.book_list_url, {"title": "Test Book"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    def test_search_books(self):
        """Test searching by title."""
        response = self.client.get(self.book_list_url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    def test_order_books(self):
        """Test ordering by publication_year."""
        Book.objects.create(
            title="Older Book", author=self.author, publication_year=2015
        )
        response = self.client.get(self.book_list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(sorted(years), years)
