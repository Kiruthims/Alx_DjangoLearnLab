from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # List all books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Retrieve a single book by ID
    path('books/create/', BookCreateView.as_view(), name='book-create'),  # Add a new book
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),  # Update a book
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),  # Delete a book
]
