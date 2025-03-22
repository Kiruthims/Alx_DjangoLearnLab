from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Comment, Post, Tag




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='',
        help_text="Enter your comment (minimum 5 characters)."
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 5:
            raise forms.ValidationError("Your comment is too short. Please enter at least 5 characters.")
        return content