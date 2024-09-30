from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from rest_framework_simplejwt.tokens import AccessToken
from users.models import UserAccount

@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user_id = token.payload['user_id']
        return UserAccount.objects.get(pk=user_id)
    except Exception as e:
        return AnonymousUser

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner
    
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        # Get the 'cookie' header
        cookie_header = headers.get(b'cookie', b'').decode()  
        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_header.split('; ')}
        
        # Retrieve the token from the cookies
        token_key = cookies.get('access')
        
        if token_key:
            # Set the user in the scope if token exists
            scope['user'] = await get_user(token_key)
        else:
            # Set user as anonymous if no token found
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)