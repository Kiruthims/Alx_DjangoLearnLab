from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import register, profile 
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    add_comment,
    comment_update,
    comment_delete,
)

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),
    path('register/', register, name = 'register'),
    path('profile/', profile, name='profile'),
    path('post/', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comments/new/', add_comment, name='add-comment'),
    path('comment/<int:comment_id>/update/', comment_update, name='comment-update'),
    path('comment/<int:comment_id>/delete/', comment_delete, name='comment-delete'),
]
