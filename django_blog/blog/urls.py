from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .models import Post
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    register,
    profile,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    search,
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
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', search, name='search'),    
    path('tags/<str:tag_name>/', lambda request, tag_name: 
         render(request, 'blog/post_list.html', 
                {'posts': Post.objects.filter(tags__name__iexact=tag_name)}), 
         name='posts-by-tag'),
]
