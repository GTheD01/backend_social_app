from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ('id', 'modified_at_formatted', 'user')

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



class MessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sent_to', 'created_by', 'created_at_formatted', 'body')


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)
    
    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages')