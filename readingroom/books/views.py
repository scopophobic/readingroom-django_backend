from django.shortcuts import render, redirect, get_object_or_404
import requests
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.views import APIView #this is for the view of API UI
from .models import Book
from .serializers import BookSerializer
# from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, permissions, status
from django.conf import settings


# def trying_fetch_book(request):
#     print(f"Request object: {request}")
#     print(f"Request method: {request.method}")
#     book_data = []

#     if request.method == "POST":

#         query = request.POST.get('query')
#         if(query):
#             api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

#             try:
#                 response = requests.get(api_url)
#                 response.raise_for_status()
#                 data = response.json()

#                 if 'items' in data :
#                     book_data = data['items']
#                 else : 
#                     messages.info(request, f"No books found for query: '{query}'" )
#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f"Error fetching data from Google Books API: {e}")
#             except Exception as e:
#                 messages.error(request, f"An unexpected error occurred: {e}")

#     return render(request, 'try_fetch_book.html',  {'books': book_data})


def fetch_books_from_api(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)

    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={settings.GOOGLE_BOOKS_API_KEY}'
    response = requests.get(url)
    return Response(response.json())


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    serializer = BookSerializer(book)
    return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter(name='q', description='Search query for books', required=True, type=str)
    ]
)
class GoogleBooksSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)

        url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={settings.GOOGLE_BOOKS_API_KEY}'
        response = requests.get(url)
        return Response(response.json())


class SaveGoogleBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if book already exists
        if Book.objects.filter(google_books_id=book_id).exists():
            return Response({'error': 'Book already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch book details from Google Books API
        url = f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={settings.GOOGLE_BOOKS_API_KEY}'
        response = requests.get(url)
        if response.status_code != 200:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        book_data = response.json()
        volume_info = book_data.get('volumeInfo', {})

        # Create book object
        book = Book.objects.create(
            title=volume_info.get('title', ''),
            author=', '.join(volume_info.get('authors', [])),
            description=volume_info.get('description', ''),
            google_books_id=book_id,
            cover_image=volume_info.get('imageLinks', {}).get('thumbnail', ''),
            added_by=request.user
        )

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'book_id'
    queryset = Book.objects.all()

    def perform_update(self, serializer):
        if serializer.instance.added_by != self.request.user:
            raise permissions.PermissionDenied("You can only edit books you added")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.added_by != self.request.user:
            raise permissions.PermissionDenied("You can only delete books you added")
        instance.delete()