from django.db import models
from django.contrib.auth.models import User
from books.models import Book 
from django.conf import settings



class Post(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    # rating = models.PositiveSmallIntegerField(null=True, blank=True)  # Optional 1–5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"
