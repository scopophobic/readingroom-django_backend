from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post
from .models import Book
# from .serializers import PostSerializer
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostCreateSerializer

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    data = request.data
    content = data.get('content')
    google_book_id = data.get('book')  # This can be None

    if not content:
        return Response({'error': 'Post content is required.'}, status=400)

    book = None
    if google_book_id:
        book = get_or_create_book(google_book_id)

    post = Post.objects.create(
        user=request.user,
        content=content,
        book=book  # Can be None
    )

    return Response({
        "message": "Post created successfully",
        "post_id": post.id
    }, status=201)



@api_view(['GET'])
def list_posts_api(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)




def get_or_create_book(google_book_id):
    from datetime import datetime
    try:
        return Book.objects.get(google_book_id=google_book_id)
    except Book.DoesNotExist:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes/{google_book_id}")
        if response.status_code == 200:
            data = response.json()
            info = data.get("volumeInfo", {})

            # Try parsing the publication date
            pub_date = info.get("publishedDate", "")
            parsed_date = None
            try:
                if len(pub_date) == 4:
                    parsed_date = datetime.strptime(pub_date, "%Y").date()
                elif len(pub_date) == 7:
                    parsed_date = datetime.strptime(pub_date, "%Y-%m").date()
                elif len(pub_date) == 10:
                    parsed_date = datetime.strptime(pub_date, "%Y-%m-%d").date()
            except Exception:
                pass

            # Create and return new book
            return Book.objects.create(
                google_book_id=google_book_id,
                title=info.get('title', 'Unknown Title')[:255],
                authors=', '.join(info.get('authors', []))[:500],
                description=info.get('description', ''),
                publication_date=parsed_date,
                cover_image_url=info.get('imageLinks', {}).get('thumbnail', '')[:2000],  # URLField has a large limit
                isbn=', '.join(
                    [i['identifier'] for i in info.get('industryIdentifiers', [])]
                )[:200] if info.get('industryIdentifiers') else '',
                publisher=info.get('publisher', '')[:255]
            )
        else:
            return None
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .forms import PostForm
# from .models import Post
# from books.models import Book

# @login_required
# def create_post(request, book_id=None):
#     book = None
#     if book_id:
#         try:
#             book = Book.objects.get(google_book_id=book_id)
#         except Book.DoesNotExist:
#             # Optional: allow creating post even if book isn't in DB
#             book = Book(google_book_id=book_id, title="Unknown Title")
#             # Don't save it unless you want to persist it

#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user
#             post.book = book  # can be None
#             post.save()
#             return redirect('home')
#     else:
#         form = PostForm()

#     return render(request, 'posts/create_post.html', {'form': form, 'book': book})





# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from books.models import Book
# from .models import Post
# from .forms import PostForm
# import requests
# from datetime import datetime

# @login_required
# def create_post(request, book_id=None):
#     book = None

#     if book_id:
#         # Try to get from DB
#         book = Book.objects.filter(google_book_id=book_id).first()

#         if not book:
#             # Fetch from Google Books API
#             response = requests.get(f"https://www.googleapis.com/books/v1/volumes/{book_id}")
#             if response.status_code == 200:
#                 data = response.json()
#                 info = data.get('volumeInfo', {})

#                 # Prepare book data
#                 title = info.get('title', 'Untitled')
#                 authors = ", ".join(info.get('authors', [])) or None
#                 description = info.get('description')
#                 pub_date = info.get('publishedDate', '')
#                 cover = info.get('imageLinks', {}).get('thumbnail')
#                 publisher = info.get('publisher')
#                 isbn = None

#                 # Extract ISBN if available
#                 for identifier in info.get('industryIdentifiers', []):
#                     if identifier.get('type') in ['ISBN_10', 'ISBN_13']:
#                         isbn = identifier.get('identifier')
#                         break

#                 # Parse publishedDate (can be yyyy-MM-dd, yyyy-MM, or yyyy)
#                 parsed_date = None
#                 try:
#                     if len(pub_date) == 4:
#                         parsed_date = datetime.strptime(pub_date, "%Y").date()
#                     elif len(pub_date) == 7:
#                         parsed_date = datetime.strptime(pub_date, "%Y-%m").date()
#                     elif len(pub_date) == 10:
#                         parsed_date = datetime.strptime(pub_date, "%Y-%m-%d").date()
#                 except Exception:
#                     pass  # invalid date format

#                 # Create book
#                 book = Book.objects.create(
#                     google_book_id=book_id,
#                     title=title,
#                     authors=authors,
#                     description=description,
#                     publication_date=parsed_date,
#                     cover_image_url=cover,
#                     isbn=isbn,
#                     publisher=publisher,
#                 )

#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user
#             post.book = book  # Optional
#             post.save()
#             return redirect('home')
#     else:
#         form = PostForm()

#     return render(request, 'posts/create_post.html', {'form': form, 'book': book})
