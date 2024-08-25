from django.urls import path
from .views import conversation_list, get_or_create_conversation, send_message, conversation_details


urlpatterns = [
    path('', conversation_list, name="conversations_list"),
    path('get-or-create/<uuid:user_id>/',  get_or_create_conversation, name='get_or_create_conversation'),
    path('send/<uuid:conversation_id>/', send_message, name='send_message'),
    path('<uuid:conversation_id>/', conversation_details, name='conversation_details')
]