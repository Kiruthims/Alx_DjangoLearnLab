from django.urls import path
from .views import BookListCreateView, BookDetailView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),  # For list and create
    path('books/create/', BookListCreateView.as_view(), name='book-create'),  # Explicit create
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # For retrieving a single book
    path('books/<int:pk>/update/', BookDetailView.as_view(), name='book-update'),  # Explicit update
    path('books/<int:pk>/delete/', BookDetailView.as_view(), name='book-delete'),  # Explicit delete
]
