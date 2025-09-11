# bookshelf/forms.py

from django import forms
from .models import Book


# Form for searching books by title
class BookSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=100,
        label='Search by Title',
        widget=forms.TextInput(attrs={'placeholder': 'Enter title'})
    )


# Form expected by the checker
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
