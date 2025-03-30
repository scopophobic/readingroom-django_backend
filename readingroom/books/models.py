from django.db import models

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)



class Book(models.Model):
     # name, author, Published Date, discription, book_id
    title = models.CharField(max_length=255)
    authors = models.CharField(blank = True, null = True)
    description = models.TextField(blank=True, null = True)
    publication_date = models.DateField(blank=True, null=True)
    cover_image_url = models.URLField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)

    google_book_id = models.CharField(max_length=255, unique = True, blank = True, null = True)

    def __str__(self):
        return self.title

