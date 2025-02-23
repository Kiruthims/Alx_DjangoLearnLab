from django.contrib import admin
from .models import Book

# Define a custom admin class for the Book model
class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'publication_year')

    search_fields = ('title', 'author')

    list_filter = ('publication_year',)

# Register the Book model with the custom admin options
admin.site.register(Book, BookAdmin)
