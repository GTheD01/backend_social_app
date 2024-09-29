from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer

# Schema for CustomTokenObtainPairView
custom_token_obtain_pair_schema = swagger_auto_schema(
        operation_id='custom_token_obtain_pair',
        operation_description='Obtain JWT tokens using email and password.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(
                description='Tokens obtained successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                    }
                ),
            ),
            400: openapi.Response(
                description='Invalid credentials'
            ),
        }
    )

# Schema for VerifyOTPView
verify_otp_schema = {
    'operation_id': 'verify_otp',
    'operation_description': 'Verify the OTP sent to the user\'s email.',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
            'otp': openapi.Schema(type=openapi.TYPE_STRING, description='One-time password sent to the email'),
        },
        required=['email', 'otp']
    ),
    'responses': {
        200: openapi.Response(
            description='Tokens issued successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                }
            ),
        ),
        404: openapi.Response(description='Invalid email or OTP.'),
        400: openapi.Response(description='Invalid OTP.'),
    }
}

# Schema for CustomTokenRefreshView
custom_token_refresh_schema = {
    'operation_id': 'refresh_token',
    'operation_description': 'Refresh the access token using the refresh token.',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
        },
        required=['refresh']
    ),
    'responses': {
        200: openapi.Response(
            description='Access token refreshed successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='New access token'),
                }
            ),
        ),
        401: openapi.Response(description='Invalid refresh token.'),
    }
}


# Schema for CustomTokenVerifyView
custom_token_verify_schema = {
    'operation_id': 'token_verify',
    'operation_description': 'Verify the provided access token.',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, description='Access token to verify'),
        },
        required=['token']
    ),
    'responses': {
        200: openapi.Response(
            description='Token is valid',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'valid': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indicates whether the token is valid'),
                }
            ),
        ),
        401: openapi.Response(description='Token is invalid.'),
    }
}


# Schema for LogoutView
logout_schema = {
    'operation_id': 'logout',
    'operation_description': 'Log out the user and clear the tokens.',
    'responses': {
        204: openapi.Response(description='Logged out successfully.'),
        401: openapi.Response(description='Unauthorized.'),
    }
}


# Schema for EditProfileView
edit_profile_schema = {
    'operation_id': 'edit_profile',
    'operation_description': 'Edit the user profile.',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='New email address'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='New username'),
        },
        required=['email', 'username']
    ),
    'responses': {
        200: openapi.Response(
            description='Profile updated successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='Updated user details'),
                }
            ),
        ),
        400: openapi.Response(description='Email or username already exists.'),
    }
}


# Schema for toggle_otp view
toggle_otp_schema = swagger_auto_schema(
    method='post',
    operation_id='toggle_otp',
    operation_description="Enable or disable multi-factor authentication (MFA) for the user.",
    responses={
        200: openapi.Response(
            description="MFA status updated",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'mfa': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="New MFA status"),
                }
            ),
        ),
    },
)

# Schema for user_details view
user_details_schema = swagger_auto_schema(
    method='get',
    operation_id='user_details',
    operation_description="Get details of a user by username.",
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_PATH, description="The username of the user", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(
            description="User details",
            schema=UserSerializer(many=False),
        ),
        404: openapi.Response(
            description="User not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                }
            ),
        ),
    },
)

# Schema for search_users view
search_users_schema = swagger_auto_schema(
    method='get',
    operation_id='search_users',
    operation_description="Search for users based on a query string.",
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(
            description="List of users matching the search query",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description="Email address"),
                        # Include other fields from the UserSerializer if needed
                    }
                ),
            ),
        ),
        204: openapi.Response(
            description="No users found"
        ),
    },
)

# Schema for follow_user view
follow_user_schema = swagger_auto_schema(
    method='post',
    operation_id='follow_user',
    operation_description="Follow or unfollow a user by username.",
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_PATH, description="The username of the user to follow/unfollow", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(
            description="Follow/Unfollow action message",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Follow or unfollow message"),
                }
            ),
        ),
        404: openapi.Response(
            description="User not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                }
            ),
        ),
    },
)
