from django.urls import path

from .views import ListNotificationsView, ReadNotificationView

urlpatterns = [
    path('', ListNotificationsView.as_view(), name="notifications"),
    path('read/<uuid:id>/', ReadNotificationView.as_view(), name='read_notification')
]