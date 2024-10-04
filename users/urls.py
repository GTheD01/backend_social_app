from django.urls import path

from .views import (
    CustomTokenObtainPairView, 
    CustomTokenRefreshView, 
    CustomTokenVerifyView, 
    LogoutView,
    EditProfileView,
    VerifyOTPView,
    ToggleOTPView,
    UserDetailsView,
    SearchUsersView,
    FollowUserView,
)



urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),

    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("toggle-mfa/", ToggleOTPView.as_view(), name='toggle_mfa'),

    path('profile/edit/', EditProfileView.as_view()),
    path('profile/details/<str:username>/', UserDetailsView.as_view(), name="user_details"),

    path('users/search/', SearchUsersView.as_view(), name="search_users"),
    path('user/follow/<str:username>/', FollowUserView.as_view(), name="follow_user"),
]