from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Book, Author

User = get_user_model()

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user (using a password that will be used with self.client.login)
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create an Author instance (ensure your Author model has a 'name' field)
        self.author = Author.objects.create(name='Test Author')
        
        # Create Book instances for testing
        self.book1 = Book.objects.create(title='Book One', publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title='Book Two', publication_year=2021, author=self.author)
        
        # Define endpoint URLs using reverse() and URL names defined in your urls.py
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})
    
    def test_list_books(self):
        # GET /api/books/ should return HTTP 200 and a list of books
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)
    
    def test_create_book_unauthenticated(self):
        # Unauthenticated POST should return HTTP 401 Unauthorized
        data = {
            'title': 'Book Three',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        # Use self.client.login to authenticate the request
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Book Three',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Book Three')
        self.client.logout()
    
    def test_retrieve_book(self):
        # GET /api/books/<pk>/ should return HTTP 200 and the correct book data
        url = self.detail_url(self.book1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_update_book_unauthenticated(self):
        # Unauthenticated PUT should return HTTP 401 Unauthorized or 403 Forbidden
        data = {
            'title': 'Updated Book One',
            'publication_year': self.book1.publication_year,
            'author': self.author.id
        }
        url = self.update_url(self.book1.pk)
        response = self.client.put(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_update_book_authenticated(self):
        # Authenticate using self.client.login, then update the book
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Updated Book One',
            'publication_year': self.book1.publication_year,
            'author': self.author.id
        }
        url = self.update_url(self.book1.pk)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book One')
        self.client.logout()
    
    def test_delete_book_unauthenticated(self):
        # Unauthenticated DELETE should return HTTP 401 Unauthorized or 403 Forbidden
        url = self.delete_url(self.book1.pk)
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_delete_book_authenticated(self):
        # Authenticate using self.client.login, then delete the book
        self.client.login(username='testuser', password='testpass')
        url = self.delete_url(self.book1.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
        self.client.logout()
    
    def test_filtering_books(self):
        # Filtering by publication_year should return only matching books
        url = f"{self.list_url}?publication_year=2020"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for book in response.data:
            self.assertEqual(book['publication_year'], 2020)
    
    def test_search_books(self):
        # Searching for "Book One" should return books with that term in the title
        url = f"{self.list_url}?search=Book One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Book One" in book['title'] for book in response.data))
    
    def test_ordering_books(self):
        # Ordering by publication_year in descending order should return books in sorted order
        url = f"{self.list_url}?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
