
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

from django.db.models import Q
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.decorators import api_view
from djoser.views import UserViewSet

from notifications.utilities import create_notification

from .serializers import UserSerializer, VerifyOTPSerializer
from users.models import UserAccount, OTP
from .forms import ProfileForm
from .docs import *

# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    @custom_token_obtain_pair_schema
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


def create_tokens(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return access_token, refresh_token


def verify_otp(user, otp):
    try:
        otp = OTP.objects.get(user=user, code=otp)

        if otp.is_expired():
            otp.delete()
            return False
        
        otp.delete()
        return True
    except OTP.DoesNotExist:
        return False


class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer
    @swagger_auto_schema(**verify_otp_schema)
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
    @swagger_auto_schema(**custom_token_refresh_schema)
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
    @swagger_auto_schema(**custom_token_verify_schema)
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get("access")

        if access_token:
            request.data['token'] = access_token

        
        return super().post(request, *args, **kwargs)
    

class LogoutView(APIView):
    @swagger_auto_schema(**logout_schema)
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
    

class EditProfileView(APIView):
    @swagger_auto_schema(**edit_profile_schema)
    def post(self, request):
        user = request.user
        email = request.data.get('email')
        username = request.data.get('username')

        if UserAccount.objects.exclude(id=user.id).filter(Q(email=email ) | Q(username=username)).exists():
            return Response({'message':"email or username already exists"})
        else:
            if request.FILES and user.avatar:
                user.avatar.delete()

            form = ProfileForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()
            
            serializer = UserSerializer(user)

            return Response({'message': 'information updated', 'user':serializer.data})
        

@toggle_otp_schema
@api_view(['POST'])
def toggle_otp(request):
    if request.user:
        request.user.mfa_enabled = not request.user.mfa_enabled
        request.user.save()

    
    return Response({"mfa":request.user.mfa_enabled},status=status.HTTP_200_OK)


@user_details_schema
@api_view(['GET'])
def user_details(request, username):
    user = UserAccount.objects.get(username=username)
    serializer = UserSerializer(user,  context={"request": request})

    return Response(serializer.data)


@search_users_schema
@api_view(["GET"])
def search_users(request):
    slug = request.GET.get('search', '')
    if slug:
        users = UserAccount.objects.filter(is_active=True, username__icontains=slug).exclude(id=request.user.id)

        serializer = UserSerializer(users, many=True, context={"request": request})

        return Response(serializer.data)

    return Response(status=status.HTTP_204_NO_CONTENT)


@follow_user_schema
@api_view(['POST'])
def follow_user(request, username):
    user = request.user
    user_to_follow = UserAccount.objects.get(username=username)

    if not user.following.contains(user_to_follow) and user.id != user_to_follow.id:
        user.following.add(user_to_follow)
        user.following_count = user.following_count + 1
        user_to_follow.followers.add(user)
        user_to_follow.followers_count = user_to_follow.followers_count + 1
        user.save()
        user_to_follow.save()
        notification = create_notification(request, 'new_follower', username=username)

        return Response({'message': "User followed"})
    else:
        user.following.remove(user_to_follow)
        user.following_count = user.following_count - 1
        user_to_follow.followers.remove(user)
        user_to_follow.followers_count = user_to_follow.followers_count - 1
        user.save()
        user_to_follow.save()
        return Response({"message": "User unfollowed"})