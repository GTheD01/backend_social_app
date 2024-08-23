import sys
from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers

import re

from .models import UserAccount


is_valid_email_regex = re.compile(r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)])')

class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    default_error_messages = {
        'email_mismatch': "Invalid email address"
    }
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ['id', 'password', 'email', 'full_name', 'username',]
    
    def validate(self, data):
        email = data.get('email')
        if is_valid_email_regex.fullmatch(email):
            return super().validate(data)
        else:
            self.fail("email_mismatch")

class UserSerializer(serializers.ModelSerializer):
    user_follows = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = ('id', 'username', 'email', 'get_avatar', 'full_name', 'posts_count', 'followers_count', 'following_count', 'user_follows')

    def to_representation(self, instance):
        if instance.is_active:
            return super().to_representation(instance)
        return None
        
    def get_user_follows(self, obj):
        if 'request' in self.context:
            req = self.context['request']
            user = req.user


            return user.following.contains(obj)
        return False

class UserDetailSerializer(serializers.ModelSerializer):
    saved_posts = serializers.SerializerMethodField()
    

    class Meta:
        model = UserAccount
        fields = fields = ('id', 'username', 'email', 'get_avatar', 'full_name', 'posts_count', 'followers_count', 'following_count', 'saved_posts',)

    def get_saved_posts(self, obj):
        from post.serializers import PostSerializer
        saved_posts = obj.saved_posts.all()
        return PostSerializer(saved_posts, many=True).data
    
    

