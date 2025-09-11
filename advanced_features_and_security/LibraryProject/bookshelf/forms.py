# bookshelf/forms.py

from django import forms

class BookSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=100,
        label='Search by Title',
        widget=forms.TextInput(attrs={'placeholder': 'Enter title'})
    )
