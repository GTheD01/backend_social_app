
from django.conf import settings

from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from djoser.views import UserViewSet

from .serializers import UserSerializer
from users.models import UserAccount
from .forms import ProfileForm

# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
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

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset


class EditProfileView(APIView):
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
                print("the form is valid")
                form.save()
            
            serializer = UserSerializer(user)

            return Response({'message': 'information updated', 'user':serializer.data})


@api_view(['GET'])
def user_details(request, username):
    user = UserAccount.objects.get(username=username)
    serializer = UserSerializer(user)

    return Response(serializer.data)


@api_view(["GET"])
def search_users(request):
    slug = request.GET.get('search', '')
    if slug:
        users = UserAccount.objects.filter(is_active=True, username__icontains=slug)

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    return Response(status=status.HTTP_204_NO_CONTENT)
