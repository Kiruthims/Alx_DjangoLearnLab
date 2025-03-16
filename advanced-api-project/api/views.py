from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from datetime import date  # Import date to use in perform_update

# ListView(retrieve all books) and CreateView (Add a new book)
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Anyone can read, only authenticated users can create

    def perform_create(self, serializer):
        """Customize behavior before saving a new book instance."""
        serializer.save(author=self.request.user)  # Automatically set the author to the logged-in user


# DetailView(retrieve a single book), UpdateView (modify book), and DeleteView (remove book)
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Read access for everyone, modification requires authentication

    def perform_update(self, serializer):
        """Customize behavior before updating an existing book instance."""
        serializer.save(last_modified=date.today())  # Automatically update last_modified date when editing
