from django.urls import path
from .views import conversation_list, get_or_create_conversation, conversation_details


urlpatterns = [
    path('', conversation_list, name="conversations_list"),
    path('get-or-create/<uuid:user_id>/',  get_or_create_conversation, name='get_or_create_conversation'),
    path('<uuid:conversation_id>/', conversation_details, name='conversation_details')
]