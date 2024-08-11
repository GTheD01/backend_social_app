from rest_framework import serializers

from .models import Post, PostAttachment, Like
from users.serializers import UserSerializer

class LikeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ('created_by')

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image')

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    user_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'body','created_by', 'created_at_formatted', 'attachments', 'likes_count', 'user_liked')
    
    def get_user_liked(self, obj):
        if self.context:
            req = self.context['request']
            user = req.user
            return obj.likes.filter(created_by=user.id).exists()