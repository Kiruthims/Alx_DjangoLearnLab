from bookshelf.models import Book

# Create a new book instance
Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Expected Output
>>> book
<Book: Book object (1)>

