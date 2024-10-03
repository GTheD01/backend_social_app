from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Notification
from .serializers import NotificationSerializer


# Create your views here.

@api_view(["GET"])
def notifications_list(request):
    user = request.user
    notifications = user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(notifications, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def read_notification(request, id):
    notification = Notification.objects.filter(created_for=request.user).get(pk=id)
    notification.is_read = True
    notification.save()

    return Response(status=status.HTTP_200_OK)