from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Authors(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    name = models.CharField(max_length=100, null=True, db_index=True)
    total_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

class Books(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    author_id = models.ForeignKey(Authors, on_delete=models.CASCADE, related_name="author_book_id",null=True)
    name = models.CharField(max_length=100, null=True, db_index=True)
    total_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

class Reviews(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    author_id = models.ForeignKey(Authors, on_delete=models.CASCADE, related_name="author_review_id",null=True)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="book_review_id", null=True)
    review = models.CharField(max_length=500, null=True, db_index=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

