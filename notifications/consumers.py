import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f"user_{self.user.id}_notifications"


        # join notification group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    
    async def disconnect(self, code):
        # leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def send_notification(self, event):
        notification = event['notification']

        await self.send(text_data=json.dumps({
            'id': notification['id'],
            'post_id': notification['post_id'],
            'body': notification['body'],
            'created_by': notification['created_by'],
            'created_for': notification['created_for'],
            'logged_in_user_notifications_count': notification['logged_in_user_notifications_count']
        }))