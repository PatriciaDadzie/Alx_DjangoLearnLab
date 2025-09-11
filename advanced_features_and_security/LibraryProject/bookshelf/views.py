# bookshelf/views.py

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .models import Book
from .forms import BookSearchForm  # You can create this form (see below)

# View to list books, requires user to be logged in and have permission.
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure view that lists all books.
    - Requires user to be logged in.
    - Requires 'can_view' permission on Book model.
    - Uses form validation to securely handle search input (avoids SQL injection).
    """
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        title = form.cleaned_data.get('title')
        if title:
            books = books.filter(title__icontains=title)

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'form': form
    })
