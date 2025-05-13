from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

schema_view = get_schema_view(
   openapi.Info(
      title="Reading Room API",
      default_version='v1',
      description="API documentation for your React frontend",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
   #  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   #  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('', views.home),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('books.urls')),
    # path('posts/', include('posts.urls')),
    path('api/users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    # path('api/posts/', include('posts.urls')),
    # path('api/books/', include('books.urls')),
    path('api/', include('comments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
