## Delete Operation

```python


# Import the Book model
from bookshelf.models import Book

# Retrieve the book to be deleted
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Try to retrieve the book again to confirm it has been deleted
try:
    book = Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Book not found!")

# Expected Output:
# Book not found!

