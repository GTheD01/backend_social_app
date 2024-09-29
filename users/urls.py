from django.urls import path

from .views import (
    CustomTokenObtainPairView, 
    CustomTokenRefreshView, 
    CustomTokenVerifyView, 
    LogoutView,
    EditProfileView,
    VerifyOTPView,

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
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

    path('logout/', LogoutView.as_view()),
    path('profile/edit/', EditProfileView.as_view()),

    path('users/search', search_users, name="search_users"),
    path('user/follow/<str:username>/', follow_user, name="follow_user"),
    path('profile/details/<str:username>/', user_details, name="user_details")
]