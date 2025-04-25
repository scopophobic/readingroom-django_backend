from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:book_id>/', views.create_post, name='create_post'),
    path('create/', views.create_post, name='create_post_no_book'),
]
