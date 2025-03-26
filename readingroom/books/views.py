from django.shortcuts import render, redirect, get_object_or_404``
import requests
from django.contrib import messages


# Create your views here.


def trying_fetch_book(request):
    print(f"Request object: {request}")
    print(f"Request method: {request.method}")
    book_data = []

    if request.method == "POST":

        query = request.POST.get('query')
        if(query):
            api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

            try:
                response = requests.get(api_url)
                response.raise_for_status()
                data = response.json()

                if 'items' in data :
                    book_data = data['items']
                else : 
                    messages.info(request, f"No books found for query: '{query}'" )
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Error fetching data from Google Books API: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'fetch_book.html',  {'books': book_data})




def book_detail(request, book_id):
    api_url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        book_info = response.json().get('volumeInfo', {})
        return render(request, 'books/book_detail.html', {'book': book_info})
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error fetching book details: {e}")
        return render(request, 'books/book_detail.html', {'error': f"Could not retrieve book details: {e}"})
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        return render(request, 'books/book_detail.html', {'error': f"An unexpected error occurred: {e}"})