from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from users.models import UserAccount
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, ConversationDetailSerializer

# Create your views here.
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



@api_view(['GET'])
def conversation_details(request, conversation_id):
    conversation = Conversation.objects.filter(users__in=[request.user]).get(pk=conversation_id)
    serializer = ConversationDetailSerializer(conversation)

    return Response(serializer.data)


@api_view(['POST'])
def send_message(request, conversation_id):
    conversation = Conversation.objects.filter(users__in=[request.user]).get(pk=conversation_id)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    
    message = Message.objects.create(
        conversation=conversation,
        body=request.data.get('message'),
        created_by=request.user,
        sent_to=sent_to
    )

    serializer = MessageSerializer(message)

    return Response(serializer.data)


@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=[request.user])
    serializer = ConversationSerializer(conversations, many=True, context={"request":request})

    return Response(serializer.data)


