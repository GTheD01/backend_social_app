from django.urls import path, include

from .views import (
    CustomTokenObtainPairView, 
    CustomTokenRefreshView, 
    CustomTokenVerifyView, 
    LogoutView,
    EditProfileView,

    toggle_otp,
    user_details,
    search_users,
    follow_user
)



urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),

    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path("toggle-mfa/", toggle_otp, name='toggle_mfa'),

    path('logout/', LogoutView.as_view()),
    path('profile/edit/', EditProfileView.as_view()),

    path('users/search', search_users, name="search_users"),
    path('user/follow/<str:username>/', follow_user, name="follow_user"),
    path('profile/details/<str:username>/', user_details, name="user_details")
]