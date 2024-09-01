from django.urls import path

from .views import notifications_list, read_notification

urlpatterns = [
    path('', notifications_list, name="notifications"),
    path('read/<uuid:id>/', read_notification, name='read_notification')
]