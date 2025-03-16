Advanced API Project
This project demonstrates the implementation of a basic CRUD API using Django REST Framework (DRF) for managing a Book model, along with its related Author model. It uses DRF's generic views and permissions to handle the basic operations: Create, Read, Update, and Delete (CRUD).

Features
ListView: Retrieves a list of all books.
DetailView: Retrieves a single book by its ID.
CreateView: Allows the creation of a new book, including linking an author.
UpdateView: Allows modification of an existing book.
DeleteView: Allows deletion of a book.
Models
Book: Represents a book in the system. It includes fields like title, description, author, and a timestamp for when it was last modified.
Author: Represents the author of a book. It is linked to books via a foreign key.
Views
The following views are implemented to handle CRUD operations:

1. BookListView: List of Books
URL: /books/
Method: GET
Permissions:
Read-only access for unauthenticated users.
Authenticated users can modify.
2. BookDetailView: Retrieve a Single Book
URL: /books/<int:pk>/
Method: GET
Permissions:
Read-only access for unauthenticated users.
3. BookCreateView: Add a New Book
URL: /books/create/
Method: POST
Permissions:
Accessible only by authenticated users.
Details:
Ensures the author field is linked to an existing author before saving the new book.
If an invalid author ID is provided, it raises a ValidationError.
4. BookUpdateView: Modify an Existing Book
URL: /books/<int:pk>/update/

Method: PUT

Permissions:

Accessible only by authenticated users.
Details:

Automatically updates the last_modified field whenever the book is modified.
5. BookDeleteView: Remove a Book
URL: /books/<int:pk>/delete/

Method: DELETE

Permissions:

Accessible only by authenticated users.
Details:

Deletes the book instance when the endpoint is accessed.
Permissions
The permissions for the views are set as follows:

IsAuthenticatedOrReadOnly: For ListView and DetailView, unauthenticated users can view the data, but authenticated users can create or modify.
IsAuthenticated: For CreateView, UpdateView, and DeleteView, only authenticated users can access the view and perform actions.

Filtering, Searching, and Ordering
The /api/books/ endpoint now supports advanced query parameters:

Filtering: Use ?publication_year=2020 to filter books by the publication year.
Searching: Use ?search=keyword to search for books by title or author name.
Ordering: Use ?ordering=title (or ?ordering=-title for descending order) to order the results.
