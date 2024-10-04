from rest_framework_simplejwt.tokens import RefreshToken
from users.models import OTP

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