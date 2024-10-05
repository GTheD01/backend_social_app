from rest_framework.generics import ListAPIView, UpdateAPIView

from .models import Notification
from .serializers import NotificationSerializer


class ListNotificationsView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.request.user.received_notifications.filter(is_read=False)


class ReadNotificationView(UpdateAPIView):
    serializer_class = NotificationSerializer
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        serializer.instance.is_read = True
        serializer.save()

    def get_queryset(self):
        return Notification.objects.filter(created_for=self.request.user)
