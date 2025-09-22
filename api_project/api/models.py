from django.db import models

class Author(models.Model):
    """
    Author model represents a writer who may have multiple books.
    Fields:
        name: Stores the name of the author.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a book written by an Author.
    Fields:
        title: Title of the book.
        publication_year: Year the book was published.
        author: ForeignKey linking the book to its author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name="books",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
