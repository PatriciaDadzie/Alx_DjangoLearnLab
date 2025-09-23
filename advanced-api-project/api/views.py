from rest_framework import generics, mixins, filters as drf_filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as django_filters 

from .models import Book
from .serializers import BookSerializer



class BookListView(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """
    ListView:
    Handles retrieving all books (GET).
    Supports filtering, searching, and ordering.
    Accessible to everyone (read-only if not authenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #  Add filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']  
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year'] 
    ordering = ['title']  # default ordering

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookCreateView(mixins.CreateModelMixin,
                     generics.GenericAPIView):
    """
    CreateView:
    Handles creating a new book (POST).
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookDetailView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """
    DetailView, UpdateView, DeleteView:
    Handles retrieving, updating, and deleting a specific book.
    Read-only for unauthenticated users,
    but authenticated users can modify or delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
