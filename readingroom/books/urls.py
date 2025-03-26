from django.urls import path 
from . import views 


urlpatterns = [
    path('fetch-books/', views.trying_fetch_book, name='fetch_books'),
    path('<str:book_id>/', views.book_detail, name='book_detail'),
]