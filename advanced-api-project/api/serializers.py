from rest_framework import serializers
from .models import Author, Book
from datetime import date # To facilitate the use of current year validation

class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model with validation for publication year."""

    def validate_publication_year(self, value):
        """Ensure publication year is not in the future."""
        current_year = date.today().year # Use current date ie today to calculate the year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model, including nested books."""
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
