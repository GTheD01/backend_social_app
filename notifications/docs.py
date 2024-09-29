from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

notifications_list_schema = swagger_auto_schema(
    method='get',
    operation_id='notifications_list',
    operation_description='Retrieve the list of unread notifications for the user.',
    responses={
        200: openapi.Response(
            description='A list of unread notifications',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Notification ID'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Notification message'),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Creation time'),
                        'is_read': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Read status of the notification'),
                    },
                ),
            ),
        ),
        401: openapi.Response(description='Unauthorized.'),
    }
)

read_notification_schema = swagger_auto_schema(
    method='post',
    operation_id='read_notification',
    operation_description='Mark a notification as read.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Notification ID'),
        },
        required=['id']
    ),
    responses={
        200: openapi.Response(description='Notification marked as read.'),
        404: openapi.Response(description='Notification not found.'),
        401: openapi.Response(description='Unauthorized.'),
    }
)

