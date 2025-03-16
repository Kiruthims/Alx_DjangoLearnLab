from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from datetime import date

# ListView - Retrieve all books
# BookListView: Retrieves all books. Accessible by both authenticated and unauthenticated users.
# Permissions: Allows only read access for unauthenticated users. Authenticated users can modify.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users, others can write

# DetailView - Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

# CreateView - Add a new book
# BookCreateView: Adds a new book. Accessible only by authenticated users.
# Permissions: Authenticated users can create new books.
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create


    def perform_create(self, serializer):
        """Customize the creation process."""
        """Ensures the author is linked before saving."""
        author_id = self.request.data.get('author')
        try:
            author = Author.objects.get(id=author_id)
            serializer.save(author=author)
        except Author.DoesNotExist:
            raise serializers.ValidationError({"author": "Invalid author ID."})


# UpdateView - Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update


    def perform_update(self, serializer):
        """Customize the update process."""
        serializer.save(last_modified=date.today())
# DeleteView - Remove a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can delete
