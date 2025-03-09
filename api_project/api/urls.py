from django .urls import path, include
from rest_framework .routers import DefaultRouter
from .views import BookList, BookSetView


router = DefaultRouter()
router.register(r'books_all', BookSetView, basename = 'book_all')

urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
        path('books/', BookList.as_view(), name = 'book-list'),
        path('', include(router.urls))
]

