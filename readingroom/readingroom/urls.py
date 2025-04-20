

from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home),
    path('auth/', include('django.contrib.auth.urls')),
    path('books/', include('books.urls')),

    path('api/users/', include('users.urls')),
    # path('api/posts/', include('posts.urls')),
    # path('api/books/', include('books.urls')),
    # path('api/comments/', include('comments.urls')),
]
