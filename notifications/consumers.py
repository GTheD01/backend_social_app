import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message


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
        
        response_data = {
            'type': notification['type'],
            'created_by': notification['created_by'],
            'created_for': notification['created_for'],
            'body': notification['body']
        }

        if notification['type'] == 'new_message':
            sent_to = notification['created_for']
            unread_conversations_count = await get_unread_conversations_count(user_id=sent_to['id'])

            response_data['unread_conversations_count'] = unread_conversations_count
            response_data['conversation_id'] = notification['conversation_id']
        else:
            response_data['id'] = notification['id']
            response_data['post_id'] = notification['post_id']
            response_data['logged_in_user_notifications_count'] = notification['logged_in_user_notifications_count']

        await self.send(text_data=json.dumps(response_data))


@sync_to_async
def get_unread_conversations_count(user_id):
    return Message.objects.filter(sent_to_id=user_id, seen=False).values('conversation').distinct().count()