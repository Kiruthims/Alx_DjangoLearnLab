from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book

def home(request):
    return HttpResponse("Welcome to the Bookshelf App!")

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        Book.objects.create(title=title, author=author, publication_year=publication_year)
        return redirect('book_list')
    return render(request, 'bookshelf/book_create.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_edit.html', {'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('book_list')