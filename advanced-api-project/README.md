Books API Documentation

Overview

A Django REST API for managing books, allowing users to create and retrieve book records. Authentication is required for certain actions.

Setup

Clone the repository:

git clone <repository-url>

Navigate to the project directory:

cd advanced-api-project

Set up a virtual environment:

python -m venv venv
source venv/bin/activate  # Windows: `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create a superuser:

python manage.py createsuperuser

Start the server:

python manage.py runserver

Authentication

Uses token-based authentication. Obtain a token with:

POST /api/token/

Include it in requests:

Authorization: Token <your_token>

Endpoints

Public Endpoints

GET /api/books/ - List books

GET /api/books/<id>/ - Retrieve a book

Authenticated Endpoints

POST /api/books/ - Create a book

Restrictions

PUT, PATCH, and DELETE are not allowed to enforce read-only access and maintain data integrity.

Notes

Ensure proper authentication for protected actions.

Use Postman.

Read-only access is available for unauthenticated users.