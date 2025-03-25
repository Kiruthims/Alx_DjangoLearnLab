Social Media API - User Authentication Setup
Overview
This document outlines the steps to set up the user authentication system for a Social Media API using Django and Django REST Framework. This API provides endpoints for user registration, login, and profile management.

Prerequisites
Python: Ensure you have Python 3.x installed.
pip:Python's package installer.

Setup Instructions
1.  Clone the Repository:
    ```bash
    git clone [https://github.com/your_username/Alx_DjangoLearnLab.git]
    cd Alx_DjangoLearnLab/social_media_api
    ```

2.  Create a Virtual Environment:
    It's highly recommended to use a virtual environment to isolate project dependencies.
        ```bash
        python3 -m venv venv_social
        source venv_social/bin/activate  # On Linux/macOS
        Windows:
        venv_social\Scripts\activate  # Command Prompt
              ```

3.  Install Dependencies:
    ```bash
    pip install django djangorestframework
    ```

4.  Configure the Database:
    The default configuration uses SQLite.  For other databases, modify the `DATABASES` setting in `social_media_api/settings.py`.
    Run migrations to create the database tables:
        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

5.  Run the Development Server:
    ```bash
    python manage.py runserver
    ```
    The server will start at `http://127.0.0.1:8000/`.

User Authentication
User Model
The `CustomUser` model is located in `accounts/models.py` and extends Django's `AbstractUser`. It includes the following fields:

 `username`:  Username for login.
 `password`:  Password for login (stored in hashed format).
 `email`: User's email address.
 `bio`:  A short biography of the user.
 `profile_picture`:  An optional profile picture.
 `followers`:  A ManyToMany field referencing itself.  This is used to store the users that a user is following. `symmetrical=False` means that if user A follows user B, user B does not automatically follow user A.

Endpoints
The following endpoints are available for user authentication:

Registration:
    URL: `POST /accounts/register/`
    Method: `POST`
    Parameters: `username`, `password`, `email` (all required), `bio` (optional), `profile_picture` (optional)
    Success Response:
        Status Code: 201 Created
        Content: `{ "token": "your_auth_token" }`
    Error Response:
        Status Code: 400 Bad Request
        Content:  A JSON object containing validation errors.

Login:
    URL: `POST /accounts/login/`
    Method: `POST`
    Parameters: `username`, `password` (both required)
    Success Response:
        Status Code: 200 OK
        Content: `{ "token": "your_auth_token" }`
    Error Response:
        Status Code: 401 Unauthorized
        Content: `{ "error": "Invalid credentials" }`

Profile:
    URL: `GET /accounts/profile/`
    Method: `GET`
    Headers:
        `Authorization`: `Token your_auth_token` (replace `your_auth_token` with the actual token)
    Success Response:
        Status Code: 200 OK
        Content:  A JSON object containing the user's profile information (id, username, email, bio, profile_picture, followers).
    Error Response:
        Status Code: 401 Unauthorized
        Content:  If the user is not authenticated.

Testing with Postman

1.  Registration:
    Open Postman.
    Create a new request.
    Set the method to `POST`.
    Enter the URL: `http://127.0.0.1:8000/accounts/register/`
    Go to the "Body" tab and select "raw" and "JSON".
    Enter the following JSON payload (replace with your desired values):
        ```json
        {
            "username": "testuser",
            "password": "testpassword",
            "email": "[email address removed]",
            "bio": "This is a test user.",
            "profile_picture": null  // Or provide a file
        }
        ```
    Click "Send".  You should receive a 201 Created response with a token.

2.  Login:
    Create a new request in Postman.
    Set the method to `POST`.
    Enter the URL: `http://127.0.0.1:8000/accounts/login/`
    Go to the "Body" tab and select "raw" and "JSON".
    Enter the following JSON payload:
        ```json
        {
            "username": "testuser",  # Use the username you registered with
            "password": "testpassword" # Use the password you registered with
        }
       ```
    Click "Send".  You should receive a 200 OK response with a token.

3.  Profile:
    Create a new request in Postman.
    Set the method to `GET`.
    Enter the URL: `http://127.0.0.1:8000/accounts/profile/`
    Go to the "Headers" tab.
    Add a header with the key `Authorization` and the value `Token your_token` (replace `your_token` with the token you received after successful registration or login).
    Click "Send".  You should receive a 200 OK response with the user's profile data.
