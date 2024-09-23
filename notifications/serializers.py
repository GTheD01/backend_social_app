from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    created_for = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = Notification
        fields = ('id', 'body', 'notification_type', 'post_id', 'created_for', 'is_read')