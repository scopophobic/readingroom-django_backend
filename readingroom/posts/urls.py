from django.urls import path
from . import views
from .views import PostCreateAPIView

urlpatterns = [
    # path('create/<str:book_id>/', views.create_post, name='create_post'),
    # path('create/', views.create_post, name='create_post_no_book'),
    path('posts/', views.list_posts_api, name='api_list_posts'),
    # path('api/posts/create/', PostCreateAPIView.as_view(), name='api_create_post'),
     path('posts/create/', views.create_post, name='create_post'),
]
