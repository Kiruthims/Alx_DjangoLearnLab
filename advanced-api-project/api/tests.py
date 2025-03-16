from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Book, Author

User = get_user_model()

class BookAPITests(TestCase):
    def setUp(self):
        # APIClient instance for sending HTTP requests
        self.client = APIClient()
        
        # Create a test user for endpoints requiring authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create an Author instance for the Book model
        self.author = Author.objects.create(name='Test Author')
        
        # Create Book instances for testing
        self.book1 = Book.objects.create(title='Book One', publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title='Book Two', publication_year=2021, author=self.author)
        
        # Define endpoint URLs using reverse() and URL names from your urls.py
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})
    
    def test_list_books(self):
        # Test GET request to list all books
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that at least 2 books are returned
        self.assertGreaterEqual(len(response.data), 2)
    
    def test_create_book_unauthenticated(self):
        # Attempt to create a book without authentication
        data = {
            'title': 'Book Three',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, format='json')
        # Expecting 401 Unauthorized because the endpoint requires authentication
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        # Authenticate and create a new book
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Book Three',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Book Three')
    
    def test_retrieve_book(self):
        # Test retrieving details of a specific book
        url = self.detail_url(self.book1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_update_book_unauthenticated(self):
        # Attempt to update a book without authentication
        data = {
            'title': 'Updated Book One',
            'publication_year': self.book1.publication_year,
            'author': self.author.id
        }
        url = self.update_url(self.book1.pk)
        response = self.client.put(url, data, format='json')
        # Expect unauthorized or forbidden status code
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_update_book_authenticated(self):
        # Authenticate and update a book
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Book One',
            'publication_year': self.book1.publication_year,
            'author': self.author.id
        }
        url = self.update_url(self.book1.pk)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book One')
    
    def test_delete_book_unauthenticated(self):
        # Attempt to delete a book without authentication
        url = self.delete_url(self.book1.pk)
        response = self.client.delete(url)
        # Expect unauthorized or forbidden status code
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_delete_book_authenticated(self):
        # Authenticate and delete a book
        self.client.force_authenticate(user=self.user)
        url = self.delete_url(self.book1.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_filtering_books(self):
        # Test filtering books by publication_year
        url = f"{self.list_url}?publication_year=2020"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for book in response.data:
            self.assertEqual(book['publication_year'], 2020)
    
    def test_search_books(self):
        # Test searching for a book by title keyword
        url = f"{self.list_url}?search=Book One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Book One" in book['title'] for book in response.data))
    
    def test_ordering_books(self):
        # Test ordering books by publication_year in descending order
        url = f"{self.list_url}?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
