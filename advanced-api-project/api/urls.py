from django.urls import path
from .views import BookListView
from .views import BookCreateView
from .views import BookDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/update/<int:pk>/', BookDetailView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', BookDetailView.as_view(), name='book-delete'),
]