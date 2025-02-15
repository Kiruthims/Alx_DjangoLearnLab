# Retrieve the book you just created
book = Book.objects.get(title="1984")
book

# Expected Output
>>> book
<Book: Book object (1)>

