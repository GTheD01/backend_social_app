import uuid

from django.db import models
from post.models import Post
from users.models import UserAccount

# Create your models here.

class Notification(models.Model):
    NEWFOLLOWER = 'new_follower'
    POST_LIKED = 'post_liked'
    POST_COMMENTED = 'post_commented'

    NOTIFICATION_TYPE_CHOICES = (
        (NEWFOLLOWER, 'New follower'),
        (POST_LIKED, 'Post liked'),
        (POST_COMMENTED, 'Post commented')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    body = models.TextField()
    created_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="created_notifications")
    created_for = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="received_notifications")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)