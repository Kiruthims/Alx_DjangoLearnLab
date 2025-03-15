from django.db import models

class Author(models.Model):
    """Model to store author details."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """Model to store book details with an author reference."""
    title = models.CharField(max_length=150)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
