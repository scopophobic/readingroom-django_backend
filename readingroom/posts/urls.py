from django.urls import path
from . import views
from .views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView

urlpatterns = [
    # New CRUD endpoints
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:post_id>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    
    # Keep existing endpoints for backward compatibility
    path('posts/create/', views.create_post, name='create_post'),
]
