from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import register, profile 
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),
    path('register/', register, name = 'register'),
    path('profile/', profile, name='profile'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/edit/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]
