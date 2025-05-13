from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post
from .models import Book
# from .serializers import PostSerializer
from rest_framework import generics, permissions, status
from .models import Post
from .serializers import PostCreateSerializer, PostSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from django.shortcuts import get_object_or_404

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'content': {
                    'type': 'string',
                    'description': 'The content of the post',
                    'example': 'This is a great book! I really enjoyed reading it.'
                },
                'book': {
                    'type': 'string',
                    'description': 'Google Books ID of the associated book (optional)',
                    'example': 'zyTCAlFPjgYC'
                }
            },
            'required': ['content']
        }
    },
    responses={
        201: {
            'description': 'Post created successfully',
            'type': 'object',
            'properties': {
                'message': {'type': 'string', 'example': 'Post created successfully'},
                'post_id': {'type': 'integer', 'example': 1}
            }
        },
        400: {
            'description': 'Bad request - Missing required fields',
            'type': 'object',
            'properties': {
                'error': {'type': 'string', 'example': 'Post content is required.'}
            }
        },
        401: {
            'description': 'Unauthorized - Authentication required'
        }
    },
    description='Create a new post. The post can optionally be associated with a book using its Google Books ID.',
    summary='Create a new post'
)
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



@extend_schema(
    responses={
        200: OpenApiResponse(
            description="List of posts retrieved successfully",
            response=PostSerializer(many=True)
        ),
        401: OpenApiResponse(description="Authentication required"),
    },
    description="Retrieve a list of all posts, ordered by creation date (newest first)",
    summary="List all posts",
    tags=["Posts"]
)
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

class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        book_id = self.request.query_params.get('book_id')
        if book_id:
            return Post.objects.filter(book_id=book_id)
        return Post.objects.all()

    def perform_create(self, serializer):
        book_id = self.request.data.get('book')
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            serializer.save(user=self.request.user, book=book)
        else:
            serializer.save(user=self.request.user)

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.all()

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own posts")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own posts")
        instance.delete()
