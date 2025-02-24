from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import UserProfile

from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Library, Book

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display details for a specific library, listing all available books in that library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Registration view as a standalone function
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})



# Helper functions to test user roles
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin view - only accessible to users with the 'Admin' role
@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Hello Admin, welcome to the admin view.")

# Librarian view - only accessible to users with the 'Librarian' role
@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse("Hello Librarian, welcome to your dashboard.")

# Member view - only accessible to users with the 'Member' role
@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Hello Member, this is the member area.")
