## Create Operation

```python


# Import the Book model
from bookshelf.models import Book

# Create a Book instance with title "1984", author "George Orwell", and publication year 1949
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Verify by printing the book to see its representation
print(book)

# Expected Output:
# <Book: 1984>
