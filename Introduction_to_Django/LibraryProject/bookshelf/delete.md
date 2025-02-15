# Delete the book you just created
from bookshelf.models import Book

book.delete()

# Expected Output
>>> Book.objects.all()
<QuerySet []>

