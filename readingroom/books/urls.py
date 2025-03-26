from django.urls import path 
from . import views 


urlpatterns = [
    path('try-fetch-books/', views.trying_fetch_book, name='try_fetch_books'), #test if the book api works
    path('fetch-books/', views.fetch_books_from_api, name='fetch_books'),
    path('<str:book_id>/', views.book_detail, name='book_detail'),
]