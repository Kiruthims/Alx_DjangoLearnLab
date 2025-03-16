from django.urls import path
from .views import BookListCreateView, BookDetailView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', BookDetailView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDetailView.as_view(), name='book-delete'),
]

