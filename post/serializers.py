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
    shared = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'body', 'created_at_formatted', 'user_liked', 'attachments', 'likes_count', 'post_saved', 'post_owner', 'comments', 'comments_count', 'created_by', 'shared')
        read_only_fields=['created_by', 'created_at']
    
    def get_shared(self, obj):
        if obj.shared:
            # check context for depth
            depth = self.context.get('depth', 1)
            # if greater than 0 serialize the shared post
            if depth > 0:
                # pass the context with decremented depth
                context = self.context.copy() # context copy
                context['depth'] = depth - 1 # decrement depth
                # Use PostSerializer to serialize the shared post
                return PostSerializer(obj.shared).data
        return None

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
        request = self.context['request']
        shared_post_id = request.data.get('shared', None)
        if shared_post_id:
            try:
                shared_post = Post.objects.get(pk=shared_post_id)
                data['shared'] = shared_post  
            except Post.DoesNotExist:
                raise serializers.ValidationError({"shared": "Invalid post ID for shared post."})

        if not data.get('body') and not data.get('shared') and not self.context['request'].FILES.getlist('image'):
            raise serializers.ValidationError("Body text or at least one image attachment is required.")
        return data
    
    def create(self, validated_data):
        attachments_data = validated_data.pop("attachments", [])
        post = Post.objects.create(**validated_data)
        for attachment_data in attachments_data:
            PostAttachment.objects.create(post=post, **attachment_data)

        return post
