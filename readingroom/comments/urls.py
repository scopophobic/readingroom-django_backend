from django.urls import path
from .views import CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
]
