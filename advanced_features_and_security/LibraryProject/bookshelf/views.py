# bookshelf/views.py

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .models import Book
from .forms import BookSearchForm, ExampleForm  # Import both forms

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
            # Filter books safely using Django ORM with parameterized queries
            books = books.filter(title__icontains=title)

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'form': form
    })

@login_required
def example_form_view(request):
    """
    Example form view demonstrating secure form handling with CSRF protection.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data here securely
            # For example, save data or perform actions
            pass
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})
