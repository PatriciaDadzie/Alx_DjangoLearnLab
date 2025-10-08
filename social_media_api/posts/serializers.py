# posts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(source='author', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'author_id', 'created_at', 'updated_at')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(source='author', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    author_profile_picture = serializers.SerializerMethodField()
    author_followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'author_id',
            'author_profile_picture',
            'author_followers_count',
            'title',
            'content',
            'comments',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'author',
            'author_id',
            'author_profile_picture',
            'author_followers_count',
            'comments',
            'created_at',
            'updated_at',
        )

    def get_author_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.author.profile_picture:
            return request.build_absolute_uri(obj.author.profile_picture.url)
        return None

    def get_author_followers_count(self, obj):
        return obj.author.followers.count()
