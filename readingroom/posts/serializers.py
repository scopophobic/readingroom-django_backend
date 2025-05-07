from rest_framework import serializers
from .models import Post

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'book', 'image']

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(author=user, **validated_data)
