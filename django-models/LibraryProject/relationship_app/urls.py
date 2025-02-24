from django.urls import path
from django.contrib.auth import views as auth_views
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view
from .views import list_books, LibraryDetailView, register

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),

    # Other URLs for your app
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Role-based access control views:
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]
