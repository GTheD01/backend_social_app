from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from djoser.views import UserViewSet
from users.serializers import UserSerializer  

class CustomUserViewSet(UserViewSet):
    # POST /users/
    @swagger_auto_schema(
        operation_description="Create a new user with the provided details.",
        request_body=UserSerializer,
        responses={
            201: 'User created successfully',
            400: 'Bad request or validation error'
        }
    )
    def create(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).create(request, *args, **kwargs)

    # POST /users/activation/
    @swagger_auto_schema(
        operation_description="Activate a user account using an activation token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_STRING, description='UID from the activation email'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='Activation token from the email'),
            },
            required=['uid', 'token']
        ),
        responses={204: 'User account activated', 400: 'Invalid activation link or token'}
    )
    def activation(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).activation(request, *args, **kwargs)

    # GET /users/me/
    @swagger_auto_schema(
        operation_description="Retrieve the currently authenticated user's information.",
        responses={200: 'Current user data retrieved', 403: 'Permission denied'}
    )
    def me(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).me(request, *args, **kwargs)

    # PUT /users/me/
    @swagger_auto_schema(
        operation_description="Update the currently authenticated user's information.",
        request_body=UserSerializer,
        responses={200: 'User updated successfully', 400: 'Invalid data'}
    )
    def update(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).me(request, *args, **kwargs)

    # PATCH /users/me/
    @swagger_auto_schema(
        operation_description="Partially update the currently authenticated user's details.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Updated username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Updated email address'),
            }
        ),
        responses={200: 'User data partially updated', 400: 'Invalid data'}
    )
    def partial_update(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).partial_update(request, *args, **kwargs)

    # DELETE /users/me/
    @swagger_auto_schema(
        operation_description="Delete the currently authenticated user's account.",
        responses={204: 'User deleted successfully', 404: 'User not found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).destroy(request, *args, **kwargs)

    # POST /users/resend_activation/
    @swagger_auto_schema(
        operation_description="Resend the activation email to a user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='The email to resend the activation to'),
            },
            required=['email']
        ),
        responses={204: 'Activation email resent', 400: 'Invalid email'}
    )
    def resend_activation(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).resend_activation(request, *args, **kwargs)


    # POST /users/reset_password/
    @swagger_auto_schema(
        operation_description="Request a password reset email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email for password reset'),
            },
            required=['email']
        ),
        responses={204: 'Password reset email sent', 400: 'Invalid email'}
    )
    def reset_password(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).reset_password(request, *args, **kwargs)

    # POST /users/reset_password_confirm/
    @swagger_auto_schema(
        operation_description="Confirm a password reset using the UID and token from the email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_STRING, description='UID from the password reset email'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='Token from the password reset email'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
            },
            required=['uid', 'token', 'new_password']
        ),
        responses={204: 'Password reset successfully', 400: 'Invalid token or UID'}
    )
    def reset_password_confirm(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).reset_password_confirm(request, *args, **kwargs)


    # GET /users/{id}/
    @swagger_auto_schema(
        operation_description="Retrieve user details by user ID.",
        responses={200: 'User details retrieved successfully', 404: 'User not found'}
    )
    def retrieve(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).retrieve(request, *args, **kwargs)

    # PUT /users/{id}/
    @swagger_auto_schema(
        operation_description="Update user details by user ID.",
        request_body=UserSerializer,
        responses={200: 'User updated successfully', 400: 'Invalid data', 404: 'User not found'}
    )
    def update(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).update(request, *args, **kwargs)

    # PATCH /users/{id}/
    @swagger_auto_schema(
        operation_description="Partially update user details by user ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Updated username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Updated email address'),
            }
        ),
        responses={200: 'User data partially updated', 400: 'Invalid data', 404: 'User not found'}
    )
    def partial_update(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).partial_update(request, *args, **kwargs)

    # DELETE /users/{id}/
    @swagger_auto_schema(
        operation_description="Delete user by user ID.",
        responses={204: 'User deleted successfully', 404: 'User not found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).destroy(request, *args, **kwargs)
