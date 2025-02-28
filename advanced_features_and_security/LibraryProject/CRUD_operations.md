# Import the Book model
from bookshelf.models import Book

# Create Operation
# Create a Book instance with title "1984", author "George Orwell", and publication year 1949
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Print the book to confirm
print(book)  # Expected Output: <Book: 1984>

# Retrieve Operation
# Retrieve the book created earlier
book = Book.objects.get(title="1984")

# Print the details of the book to confirm
print(book)  # Expected Output: <Book: 1984>

# Update Operation
# Retrieve the book to be updated
book = Book.objects.get(title="1984")

# Update the book's title
book.title = "Nineteen Eighty-Four"
book.save()

# Print the updated book to verify the change
print(book)  # Expected Output: <Book: Nineteen Eighty-Four>

# Delete Operation
# Retrieve the book to be deleted
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Try to retrieve the book again to confirm it has been deleted
try:
    book = Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Book not found!")  # Expected Output: Book not found!
