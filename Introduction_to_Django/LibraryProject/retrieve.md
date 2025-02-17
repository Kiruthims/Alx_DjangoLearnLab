## Retrieve Operation

```python


# Import the Book model
from bookshelf.models import Book

# Retrieve the book created earlier
book = Book.objects.get(title="1984")

# Print the details of the book to confirm
print(book)

# Expected Output:
# <Book: 1984>
