from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'created_at')  # Show post ID and other useful info
    list_filter = ('created_at', 'user')  # Optional: filtering options
    search_fields = ('content', 'user__username')  # Optional: search bar

# OR if you're not using the decorator
# admin.site.register(Post, PostAdmin)
