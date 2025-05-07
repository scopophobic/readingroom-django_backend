from rest_framework import serializers
from .models import Book, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = '__all__'
