from django.shortcuts import render, redirect, get_object_or_404 # to render templates for various views and also redrct after success
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm  # required for user registr
from django.contrib.auth.decorators import login_required #to protect a view from unauthenticated usrs
from django.contrib.auth import login #to login users after regstn
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin




def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Logs in the user after regstrn
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect("home")  # Redirect to home
        else:
            messages.error(request, "There was an error with your registration. Please try again.")    
    else:
        form = CustomUserCreationForm()
    
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)


    # List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  
    context_object_name = 'posts'
    ordering = ['-published_date']  # Newest posts first

# Display a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Create a new post (authenticated users only)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']  # The form will include these fields
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        # Automatically set the author to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update an existing post (only the post author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Only allow the author to update the post
        post = self.get_object()
        return self.request.user == post.author

# Delete a post (only the post author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'  # Redirect to home after deletion
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def add_comment(request, post_pk):
    """
    View to handle adding a comment to a specific post.
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment was added.")
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})


@login_required
def comment_update(request, comment_id):
    """
    View to update a comment. Only the comment author can update.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "You cannot edit this comment.")
        return redirect('post-detail', pk=comment.post.pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_delete(request, comment_id):
    """
    View to delete a comment. Only the comment author can delete.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "You cannot delete this comment.")
        return redirect('post-detail', pk=comment.post.pk)
    
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('post-detail', pk=comment.post.pk)
    
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})

