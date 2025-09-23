from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# List all books or create a new book
class BookListCreateView(generics.ListCreateAPIView):
    """
    Handles listing all books (GET) and creating a new book (POST).
    Unauthenticated users can view books,
    but only authenticated users can create new ones.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Retrieve, update, or delete a single book by ID
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving (GET), updating (PUT/PATCH),
    and deleting (DELETE) a specific book by ID.
    Only authenticated users can modify or delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
