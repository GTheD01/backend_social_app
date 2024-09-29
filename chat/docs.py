from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Swagger auto schema for get_or_create_conversation view
get_or_create_conversation_schema = swagger_auto_schema(
    methods=['GET'],
    operation_id='get_or_create_conversation',
    operation_description='Retrieve or create a conversation between the current user and another user.',
    responses={
        200: openapi.Response(
            description='Conversation details',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Conversation ID'),
                    'users': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER, description='User IDs involved in the conversation')
                    ),
                    'messages': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Message ID'),
                                'body': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
                                'created_by': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the message sender'),
                                'sent_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the message recipient'),
                                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Message creation timestamp'),
                                'seen': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Message seen status'),
                            }
                        )
                    ),
                },
            ),
        ),
        404: openapi.Response(description='User not found.'),
    }
)

# Swagger auto schema for conversation_details view
conversation_details_schema = swagger_auto_schema(
    methods=['GET'],
    operation_id='conversation_details',
    operation_description='Retrieve details of a specific conversation.',
    responses={
        200: openapi.Response(
            description='Conversation details',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Conversation ID'),
                    'users': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER, description='User IDs involved in the conversation')
                    ),
                    'messages': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Message ID'),
                                'body': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
                                'created_by': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the message sender'),
                                'sent_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the message recipient'),
                                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Message creation timestamp'),
                                'seen': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Message seen status'),
                            }
                        )
                    ),
                },
            ),
        ),
        404: openapi.Response(description='Conversation not found.'),
    }
)

# Swagger auto schema for send_message view
send_message_schema = swagger_auto_schema(
    methods=['POST'],
    operation_id='send_message',
    operation_description='Send a message in a conversation.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
        },
        required=['message']
    ),
    responses={
        200: openapi.Response(
            description='Message sent successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Message ID'),
                    'body': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
                    'created_by': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the message sender'),
                    'sent_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the message recipient'),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Message creation timestamp'),
                    'seen': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Message seen status'),
                }
            ),
        ),
        400: openapi.Response(description='Message content is required.'),
        404: openapi.Response(description='Conversation not found.'),
    }
)

# Swagger auto schema for conversation_list view
conversation_list_schema = swagger_auto_schema(
    methods=['GET'],
    operation_id='conversation_list',
    operation_description='Retrieve a list of conversations for the current user.',
    responses={
        200: openapi.Response(
            description='List of conversations',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Conversation ID'),
                        'users': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_INTEGER, description='User IDs involved in the conversation')
                        ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Message ID'),
                                    'body': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
                                    'created_by': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the message sender'),
                                    'sent_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the message recipient'),
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Message creation timestamp'),
                                    'seen': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Message seen status'),
                                }
                            )
                        ),
                    },
                ),
            ),
        ),
    }
)
