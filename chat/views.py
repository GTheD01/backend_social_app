from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from users.models import UserAccount
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, ConversationDetailSerializer
from .docs import *

# Create your views here.

@get_or_create_conversation_schema
@api_view(['GET'])
def get_or_create_conversation(request, user_id):
    user = UserAccount.objects.get(pk=user_id)
    conversations = Conversation.objects.filter(users__in=[request.user]).filter(users__in=[user])

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()
    

    serializer = ConversationDetailSerializer(conversation)

    return Response(serializer.data)


@conversation_details_schema
@api_view(['GET'])
def conversation_details(request, conversation_id):
    conversation = Conversation.objects.filter(users__in=[request.user]).get(pk=conversation_id)
    for message in conversation.messages.exclude(created_by=request.user.id):
        if not message.seen:
            message.seen = True
            message.save()

    serializer = ConversationDetailSerializer(conversation)


    return Response(serializer.data)

@conversation_list_schema
@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=[request.user])
    serializer = ConversationSerializer(conversations, many=True, context={"request":request})


    return Response(serializer.data)


