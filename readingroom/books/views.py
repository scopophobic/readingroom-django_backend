from django.shortcuts import render, redirect, get_object_or_404
import requests
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.views import APIView #this is for the view of API UI
from .models import Book
from .serializers import BookSerializer
# from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.utils import extend_schema, OpenApiParameter
# Create your views here.


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
    book_data = None
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                data = response.json()

                if 'items' in data:
                    book_data = data['items']
                else:
                    messages.info(request, f"No books found for query: '{query}'")

            except requests.exceptions.RequestException as e:
                messages.error(request, f"Error fetching data from Google Books API: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'fetch_book.html', {'book_data': book_data})


def book_detail(request, book_id):
    api_url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        book_info = response.json().get('volumeInfo', {})
        # In the future, for your API, you might return this book_info as a JSON response
        return render(request, 'book_details.html', {'book': book_info})
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error fetching book details: {e}")
        return render(request, 'book_details.html', {'error': f"Could not retrieve book details: {e}"})
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        return render(request, 'book_details.html', {'error': f"An unexpected error occurred: {e}"})


@extend_schema(
    parameters=[
        OpenApiParameter(name='q', description='Search query for books', required=True, type=str)
    ]
)
class GoogleBooksSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({'error': 'Query parameter `q` is required'}, status=400)

        url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
        response = requests.get(url)

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch from Google Books'}, status=500)

        books = []
        for item in response.json().get('items', []):
            info = item['volumeInfo']
            books.append({
                'google_book_id': item['id'],
                'title': info.get('title'),
                'authors': ', '.join(info.get('authors', [])),
                'description': info.get('description'),
                'publication_date': info.get('publishedDate'),
                'cover_image_url': info.get('imageLinks', {}).get('thumbnail'),
                'publisher': info.get('publisher'),
                'isbn': next((id['identifier'] for id in info.get('industryIdentifiers', []) if id['type'] == 'ISBN_13'), None),
            })

        return Response(books, status=200)
    


class SaveGoogleBookView(APIView):
    # permission_classes = [IsAuthenticated]  # enable if auth is required

    def post(self, request):
        data = request.data

        google_book_id = data.get('google_book_id')
        if not google_book_id:
            return Response({'error': 'google_book_id is required'}, status=400)

        # Prevent duplicate entry
        if Book.objects.filter(google_book_id=google_book_id).exists():
            return Response({'message': 'Book already exists'}, status=200)

        book = Book.objects.create(
            title=data.get('title'),
            authors=data.get('authors'),
            description=data.get('description'),
            publication_date=data.get('publication_date', None),
            cover_image_url=data.get('cover_image_url'),
            publisher=data.get('publisher'),
            isbn=data.get('isbn'),
            google_book_id=google_book_id,
        )

        serializer = BookSerializer(book)
        return Response(serializer.data, status=201)