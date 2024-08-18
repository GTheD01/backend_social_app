from django.urls import path, include

from .views import (
    CustomTokenObtainPairView, 
    CustomTokenRefreshView, 
    CustomTokenVerifyView, 
    LogoutView,
    EditProfileView,
    CustomUserViewSet,
    user_details,
    search_users
)



urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/edit/', EditProfileView.as_view()),
    path('users/', CustomUserViewSet.as_view({'get':'list'}), name='user-list'),
    path('users/search', search_users, name="search_users"),
    path('profile/details/<str:username>/', user_details, name="user_details")
]