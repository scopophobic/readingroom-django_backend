from django.urls import path
from . import views
from .views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    GoogleBooksSearchView,
    SaveGoogleBookView
)

urlpatterns = [
    # New CRUD endpoints
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<str:book_id>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    
    # Google Books API endpoints
    path('books/search/', GoogleBooksSearchView.as_view(), name='book-search'),
    path('books/save/', SaveGoogleBookView.as_view(), name='book-save'),
    
    # Keep existing endpoints for backward compatibility
    path('fetch-books/', views.fetch_books_from_api, name='fetch_books'),
]