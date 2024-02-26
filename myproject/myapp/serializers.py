from rest_framework import serializers
from . models import *

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = [
            'id',
            'name',
            'total_rating'
        ]



class BookSerializer(serializers.ModelSerializer):
    author_details = AuthorSerializer(source='author_id', read_only=True)
    class Meta:
        model = Books
        fields = [
            'id',
            'name',
            'total_rating',
            'author_details'
        ]

class ReviewAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = [
            'id',
            'review',
            'rating'
        ]
