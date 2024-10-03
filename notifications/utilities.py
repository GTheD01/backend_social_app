from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification
from post.models import Post
from users.models import UserAccount


def create_notification(request, notification_type, post_id=None, username=None):
    created_for = None

    if notification_type == "post_liked":
        body = f"{request.user.username} liked one of your posts"
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif notification_type == "post_commented":
        body = f"{request.user.username} commented on one of your posts"
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif notification_type == "new_follower":
        user = UserAccount.objects.get(username=username)
        created_for = user
        body = f"{request.user.username} has followed you."

    
    notification = Notification.objects.create(
        body=body,
        notification_type=notification_type,
        created_by=request.user,
        post_id = post_id,
        created_for = created_for
    )

    channel_layer = get_channel_layer()
    notifications_count = created_for.received_notifications.filter(is_read=False).count()


    async_to_sync(channel_layer.group_send)(
        f"user_{created_for.id}_notifications",
        {
            "type": "send_notification",
            'notification': {
                'id': str(notification.id),
                "post_id": str(post_id),
                'body': notification.body,
                'created_by': notification.created_by.username,
                'created_for': notification.created_for.username,
                'logged_in_user_notifications_count': notifications_count
            }
        }
    )

    return notification