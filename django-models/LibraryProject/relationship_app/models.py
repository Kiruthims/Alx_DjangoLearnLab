from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book)
    
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

    #UserProfile model to extend the built-in user model
class UserProfile(models.Model):
        ROLE_CHOICES = (
            ('Admin', 'Admin'),
            ('Librarian', 'Librarian'),
            ('Member', 'Member'),
        )

        user = models.OneToOneField(User, on_delete=models.CASCADE)
        role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Member')

        def __str__(self):
          return f"{self.user.username} - {self.role}"
        

    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Default new users to 'Member' role
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()    
