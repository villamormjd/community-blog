from rest_framework import serializers
from .models import Blogs, Comment
from users.serializers import UserSerializer


class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ['id', 'title', 'content', 'author_id', 'created_on', 'modified_on']
        extra_kwargs = {
            'author_id': {
                'required': False
            }
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['author'] = UserSerializer(instance.author_id).data
        return response


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'blog_id', 'comment_author_id', 'created_on', 'modified_on']
        extra_kwargs = {
            'blog_id': {
                'required': False
            },
            'comment_author_id': {
                'required': False
            }
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['blog'] = BlogSerializers(instance.blog_id).data
        response['comment_author'] = UserSerializer(instance.comment_author_id).data
        return response
