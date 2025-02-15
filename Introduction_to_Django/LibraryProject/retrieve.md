# Retrieve the book you just created
book = Book.objects.get(id=1)
book

# Expected Output
>>> book
<Book: Book object (1)>

