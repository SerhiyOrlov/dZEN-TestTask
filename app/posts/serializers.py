from rest_framework import serializers
from .models import Post, Comment
import bleach


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['created_at']


ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'a']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'author', 'parent', 'created_at']
        read_only_fields = ['created_at']

    def validate_text(self, value):
        # Удаление всех HTML тегов, кроме разрешенных
        return self._clean_text(value)

    def _clean_text(self, value):
        return bleach.clean(value, tags=ALLOWED_TAGS, strip=True)


class CommentReplSerializer(serializers.ModelSerializer):
    post = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'author', 'parent', 'created_at']
        read_only_fields = ['created_at']

    def validate_text(self, value):
        # Удаление всех HTML тегов, кроме разрешенных
        return self._clean_text(value)

    def _clean_text(self, value):
        return bleach.clean(value, tags=ALLOWED_TAGS, strip=True)


class CommentReplySerializer(CommentSerializer):
    post = serializers.CharField(read_only=True)

    class Meta(CommentSerializer.Meta):
        pass