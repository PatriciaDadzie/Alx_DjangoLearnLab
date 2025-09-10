# bookshelf/views.py

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .models import Book

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
