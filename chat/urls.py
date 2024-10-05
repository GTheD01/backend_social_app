from django.urls import path
from .views import ConversationDetailsView, GetOrCreateConversationView, ListConversationsView


urlpatterns = [
    path('', ListConversationsView.as_view(), name="conversations_list"),
    path('get-or-create/<uuid:user_id>/',  GetOrCreateConversationView.as_view(), name='get_or_create_conversation'),
    path('<uuid:conversation_id>/', ConversationDetailsView.as_view(), name='conversation_details')
]