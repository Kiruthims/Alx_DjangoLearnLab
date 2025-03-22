from django.shortcuts import render, redirect, get_object_or_404 # to render templates for various views and also redrct after success
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm,PostForm # required for user registr
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
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        # Automatically set the author to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update an existing post (only the post author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
       
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


def search(request):
    query = request.GET.get('q', '')
    results = Post.objects.all()
    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()  # To avoid duplication if multiple tags match
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'blog/search_results.html', context)