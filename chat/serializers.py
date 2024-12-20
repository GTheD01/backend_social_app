from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sent_to', 'created_by', 'created_at_formatted', 'body', 'seen')


class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    last_received_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ('id', 'modified_at_formatted', 'user', 'last_received_message',)
    

    def get_last_received_message(self, obj):
        if self.context:
            req = self.context['request']
            user = req.user
            message = obj.messages.last()
            if message:
                value = None
                if message.created_by.username == user.username:
                    value = {'last_message': f"You: {message.body}", 'seen': True}
                else:
                    value = {"last_message": f"{message.created_by.username}: {message.body}", "seen": message.seen}
                return value
            
            return {"last_message": None, 'seen': False}
        


    def get_user(self, obj):
        if self.context:
            req = self.context['request']
            user = req.user
            other_user = obj.users.exclude(id=user.id)
            if other_user.exists():
                serializer = UserSerializer(other_user.first())
                return serializer.data
            else:
                return


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)
    users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages')