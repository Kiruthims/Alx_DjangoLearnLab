import os
import django
import sys

# Set up the environment by adding the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)   
    books = Book.objects.filter(author=author)       
    return [book.title for book in books]

# List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return [book.title for book in library.books.all()]

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    library_obj = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library_obj)
    return librarian.name

#if __name__ == '__main__':
 #   # Sample function calls
  #  print("Books by J.K. Rowling:", get_books_by_author("J.K. Rowling"))
   # print("Books in City Library:", get_books_in_library("City Library"))
    #print("Librarian for City Library:", get_librarian_for_library("City Library"))
