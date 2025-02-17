
## Update Operation

```python


# Import the Book model
from bookshelf.models import Book

# Retrieve the book to be updated
book = Book.objects.get(title="1984")

# Update the book's title
book.title = "Nineteen Eighty-Four"
book.save()

# Print the updated book to verify the change
print(book)

# Expected Output:
# <Book: Nineteen Eighty-Four>
