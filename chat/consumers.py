import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from notifications.utilities import create_message_notification

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from web sockets
    async def receive(self, text_data):
        data = json.loads(text_data)

        conversation_id = data['data']['conversation_id']
        sent_to = data['data']['sent_to']
        name = data['data']['name']
        body = data['data']['body']

        message = await self.save_message(conversation_id, body, sent_to)
        # If the message was saved successfully, send it to the group
        if message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'body': body,
                    'name': name,
                    'message_id': str(message.id),
                    'created_at': str(message.created_at_formatted()),
                    'created_by_id': str(message.created_by.id),
                    'conversation_id': conversation_id
                }
            )

    # send messages
    async def chat_message(self, event):
        body = event['body']
        name = event['name']
        message_id = event['message_id']
        created_at = event['created_at']
        created_by_id = event['created_by_id']
        conversation_id = event['conversation_id']

        await self.send(text_data=json.dumps({
            'body': body,
            'name': name,
            'message_id': str(message_id),
            'created_at': str(created_at),
            "created_by_id": created_by_id,
            'conversation_id': conversation_id
        }))

    @sync_to_async
    def save_message(self, conversation_id, body, sent_to):
        user = self.scope['user']
        create_message_notification(user, sent_to, conversation_id, body)
        return Message.objects.create(conversation_id=conversation_id, body=body, sent_to_id=sent_to['id'], created_by=user)
    