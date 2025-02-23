import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    books = Book.objects.filter(author__name=author_name)
    return [book.title for book in books]

# List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return [book.title for book in library.books.all()]

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    librarian = Librarian.objects.get(library__name=library_name)
    return librarian.name if librarian else "No librarian found"

# Sample function calls
#if __name__ == "__main__":
 #   print("Books by J.K. Rowling:", get_books_by_author("J.K. Rowling"))
  #  print("Books in City Library:", get_books_in_library("City Library"))
   # print("Librarian for Central Library:", get_librarian_for_library("Central Library"))
