from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import BookForm
from .models import Library, Book
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils.html import escape

def list_books(request):
    """
    Lists all books, with search functionality.
    Secured against SQL injection by using ORM and sanitizing input.
    """
    search_term = request.GET.get('q')  
    if search_term:
        search_term = escape(search_term)  
        books = Book.objects.filter(title__icontains=search_term)  
    else:
        books = Book.objects.all()

    return render(request, 'relationship_app/list_books.html', {'books': books, 'search_term': search_term})
class LibraryDetailView(DetailView):
    """
    Displays details of a library. Safe as it uses Django's DetailView.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    """
    Handles user registration. Uses UserCreationForm for secure form handling.
    Prevents SQL injection and XSS through form validation.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def is_admin(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin view. No user input or database interaction, so no security concerns.
    """
    return render(request, 'relationship_app/admin_view.html')

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian view. No user input or database interaction, so no security concerns.
    """
    return render(request, 'relationship_app/librarian_view.html')

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    """
    Member view. No user input or database interaction, so no security concerns.
    """
    return render(request, 'relationship_app/member_view.html')

def login_view(request):
    """
    Handles user login. Uses AuthenticationForm for secure form handling.
    Prevents SQL injection and XSS through form validation.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('admin_view'))
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    Adds a book. Uses BookForm for secure form handling.
    Prevents SQL injection and XSS through form validation.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """
    Edits a book. Uses BookForm for secure form handling.
    Prevents SQL injection and XSS through form validation.
    """
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form})

from django.shortcuts import get_object_or_404
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """
    Deletes a book. Uses get_object_or_404 and book.delete() for secure deletion.
    Prevents SQL injection.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/confirm_delete.html', {'book': book})