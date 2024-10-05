from django.contrib.auth import get_user_model

from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Conversation
from .serializers import ConversationSerializer, ConversationDetailSerializer

UserAccount = get_user_model()


class GetOrCreateConversationView(GenericAPIView):
    serializer_class = ConversationDetailSerializer

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(UserAccount, id=user_id)
        conversation = Conversation.objects.filter(users__in=[request.user, user]).annotate(user_count=Count('users')).filter(user_count=2).first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.users.add(user, request.user)
            conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)
    

class ConversationDetailsView(RetrieveAPIView):
    serializer_class = ConversationDetailSerializer
    lookup_field = 'conversation_id'

    def get_object(self):
        conversation_id = self.kwargs['conversation_id']
        conversation = get_object_or_404(Conversation, id=conversation_id, users=self.request.user)

        unseen_messages = conversation.messages.exclude(created_by=self.request.user.id)
        unseen_messages.update(seen=True)

        return conversation
    
    def get(self, request, *args, **kwargs):
        conversation = self.get_object()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)


class ListConversationsView(ListAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(users=self.request.user)
    