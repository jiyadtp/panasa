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