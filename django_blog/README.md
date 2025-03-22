Authentication System Documentation
1. Overview
This authentication system allows users to register, log in, log out, and manage their profiles. It uses Django’s built-in authentication views and custom forms for profile management.

2. Authentication Features
a) User Registration
Users can sign up by providing their email and password.

The registration form uses Django’s UserCreationForm with custom fields.

After successful registration, the user is redirected to the login page.

How to Test Registration:
Go to /register/.

Enter an email and a secure password.

Submit the form.

If successful, you should be redirected to the login page.

b) User Login
Users can log in using their email and password.

Django’s built-in LoginView is used.

A session is created upon successful login.

How to Test Login:
Go to /login/.

Enter valid credentials.

Click "Login."

You should be redirected to the profile page.

Try logging in with incorrect credentials to check error handling.

c) User Logout
Users can log out using Django’s LogoutView.

Upon logging out, they are redirected to the logout confirmation page.

How to Test Logout:
Log in first.

Go to /logout/.

You should see a logout confirmation message.

Try accessing /profile/—it should redirect you to login.

d) Profile Management
Users can update their email, bio, and profile picture.

Uses a custom UserProfileForm and UserUpdateForm.

How to Test Profile Management:
Log in.

Go to /profile/.

Update your email, bio, or profile picture.

Submit the form and check if the changes are saved.

3. Error Handling
Incorrect login attempts display an error message.

Validation errors appear if registration details are invalid.

Profile update errors are shown next to invalid fields.

4. Additional Notes
CSRF protection is enabled for all forms.

Users must be logged in to access /profile/.

Logout clears the session and prevents access to restricted pages.

 Blog Post Management
- List View: Accessible at `/posts/`, shows all posts.
- Detail View: Accessible at `/posts/<post_id>/`.
- Create Post: Authenticated users can create new posts at `/posts/new/`.
- Update Post: Only the post author can edit at `/posts/<post_id>/edit/`.
- Delete Post: Only the post author can delete at `/posts/<post_id>/delete/`.

 Testing Instructions
1. Register a new user and log in.
2. Create a new blog post.
3. View, update, and delete the blog post.
4. Try accessing update/delete views as a non-author to verify permissions.
