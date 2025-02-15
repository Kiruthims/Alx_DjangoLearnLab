# CRUD Operations in Django

```python
# 1. Create Book Instance

from bookshelf.models import Book

# Create a new book instance
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Expected Output:
>>> book
<Book: Book object (1)>

# ----------------------------

# 2. Retrieve Book Instance

book = Book.objects.all()

# Expected Output:
>>> book
<QuerySet [<Book: Book object (1)>]>

# ----------------------------

# 3. Update Book Instance

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Expected Output:
>>> book
<Book: Book object (1)>

# ----------------------------

# 4. Delete Book Instance

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Expected Output:
>>> book
1

