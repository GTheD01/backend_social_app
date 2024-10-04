
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListAPIView
from djoser.views import UserViewSet

from notifications.utilities import create_notification

from users.models import OTP
from .serializers import ProfileSerializer, UserSerializer, VerifyOTPSerializer

from .utils import create_tokens, verify_otp

UserAccount = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            email = request.data.get("email")
            user = UserAccount.objects.get(email=email)

            if user.mfa_enabled:
                otp = OTP.objects.create(user=user)
                subject = "OTP Code"
                message = f"Your verification code is:{otp.code}"
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient_list=[user.email]
                send_mail(subject, message, email_from, recipient_list)
                return Response({"message": "OTP sent to your email. Please verify.", "otp":True}, status=status.HTTP_206_PARTIAL_CONTENT)

            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
        
            response.set_cookie(
                'access', 
                access_token, 
                max_age=settings.AUTH_COOKIE_MAX_AGE, 
                path=settings.AUTH_COOKIE_PATH, 
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh', 
                refresh_token, 
                max_age=settings.AUTH_COOKIE_MAX_AGE, 
                path=settings.AUTH_COOKIE_PATH, 
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        email=request.data.get("email")
        otp = request.data.get('otp')

        try:
            user = UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            return Response({"message": "Invalid email or OTP."}, status=status.HTTP_404_NOT_FOUND)

        if verify_otp(user, otp):  
            access_token, refresh_token = create_tokens(user)

            response = Response({"access": access_token, "refresh": refresh_token})
            response.set_cookie(
                'access', 
                access_token, 
                max_age=settings.AUTH_COOKIE_MAX_AGE, 
                path=settings.AUTH_COOKIE_PATH, 
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh', 
                refresh_token, 
                max_age=settings.AUTH_COOKIE_MAX_AGE, 
                path=settings.AUTH_COOKIE_PATH, 
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            
            return response
        else:
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data['refresh'] = refresh_token
        
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")

            response.set_cookie(
                'access', 
                access_token, 
                max_age=settings.AUTH_COOKIE_MAX_AGE, 
                path=settings.AUTH_COOKIE_PATH, 
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get("access")

        if access_token:
            request.data['token'] = access_token

        
        return super().post(request, *args, **kwargs)
    

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)

        response.set_cookie(
                'access', 
                '', 
                max_age=0, 
                expires='Thu, 01 Jan 1970 00:00:00 GMT',
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        
        response.set_cookie(
            'refresh', 
            '', 
            max_age=0, 
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
            path=settings.AUTH_COOKIE_PATH, 
            secure=settings.AUTH_COOKIE_SECURE, 
            httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
            samesite=settings.AUTH_COOKIE_SAMESITE
        )

        return response


class CustomUserViewSet(UserViewSet):
    queryset = UserAccount.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset


class EditProfileView(UpdateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.FILES and user.avatar:
            user.avatar.delete()
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Information updated', 'user': serializer.data}, status=status.HTTP_200_OK)
        

class ToggleOTPView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user

        if user:
            user.mfa_enabled = not user.mfa_enabled
            user.save()

            return Response({"mfa":request.user.mfa_enabled},status=status.HTTP_200_OK)      
        

class UserDetailsView(RetrieveAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class SearchUsersView(ListAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        slug = self.request.query_params.get("search", None)
        if slug:
            return UserAccount.objects.filter(is_active=True, username__icontains=slug).exclude(id=self.request.user.id)
        return UserAccount.objects.none()


class FollowUserView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        username = self.kwargs['username']
        user_to_follow = get_object_or_404(UserAccount, username=username)

        if not user.following.contains(user_to_follow) and user.id != user_to_follow.id:
            user.following.add(user_to_follow)
            user.following_count += 1
            user_to_follow.followers.add(user)
            user_to_follow.followers_count += 1
            user.save()
            user_to_follow.save()
            notification = create_notification(request, 'new_follower', username=username)

            return Response({'message': "User followed"})
        else:
            user.following.remove(user_to_follow)
            user.following_count -=1
            user_to_follow.followers.remove(user)
            user_to_follow.followers_count -= 1
            user.save()
            user_to_follow.save()
            
            return Response({"message": "User unfollowed"})
