from rest_framework import serializers

from .models import Post, PostAttachment, Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comment_owner = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted', 'comment_owner')

    def get_comment_owner(self, obj):
        if self.context:
            req = self.context['request']
            user = req.user
            return obj.created_by.id == user.id


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image')

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)
    user_liked = serializers.SerializerMethodField()
    post_saved = serializers.SerializerMethodField()
    post_owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'body', 'created_at_formatted', 'user_liked', 'attachments', 'likes_count', 'post_saved', 'post_owner', 'comments', 'comments_count', 'created_by')
        read_only_fields=['created_by', 'created_at']
    

    def get_user_liked(self, obj):
        if self.context:
            req = self.context['request']
            user = req.user 

            return obj.likes.filter(id=user.id).exists()
    
    def get_post_saved(self, obj):
        if self.context:
            req = self.context['request']
            user = req.user
            return user.saved_posts.filter(pk=obj.id).exists()
    
    def get_post_owner(self, obj):
        if self.context:
            req = self.context['request']
            user = req.user
            return obj.created_by == user
        
    def validate(self, data):
        if not data.get('body') and not self.context['request'].FILES.getlist('image'):
            raise serializers.ValidationError("Body text or at least one image attachment is required.")
        return data
    
    def create(self, validated_data):
        attachments_data = validated_data.pop("attachments", [])
        post = Post.objects.create(**validated_data)
        for attachment_data in attachments_data:
            PostAttachment.objects.create(post=post, **attachment_data)

        return post
