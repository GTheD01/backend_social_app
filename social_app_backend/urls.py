"""social_app_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny


from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from .docs import CustomUserViewSet


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Socializing API",
        default_version="1.0.0",
        description="API documentation of Socializing"
    ),
    public=True,
    permission_classes=[AllowAny]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/posts/", include('post.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/', include('users.urls')),
    path("swagger/schema/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-schema"),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path("api/", include('djoser.urls')),
    path('api/users/', CustomUserViewSet.as_view({'post': 'create'}), name='user-list-create'),
    path('api/users/me/', CustomUserViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-me'),
    path('api/users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
    path('api/users/activation/', CustomUserViewSet.as_view({'post': 'activation'}), name='user-activation'),
    path('api/users/resend_activation/', CustomUserViewSet.as_view({'post': 'resend_activation'}), name='user-resend-activation'),
    path('api/users/reset_password/', CustomUserViewSet.as_view({'post': 'reset_password'}), name='user-reset-password'),
    path('api/users/reset_password_confirm/', CustomUserViewSet.as_view({'post': 'reset_password_confirm'}), name='user-reset-password-confirm'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)