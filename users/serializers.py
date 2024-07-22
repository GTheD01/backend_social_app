from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers

import re

is_valid_email_regex = re.compile(r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)])')

class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    default_error_messages = {
        'email_mismatch': "Invalid email address"
    }
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ['id', 'password', 'email', 'first_name', 'last_name']
    
    def validate(self, data):
        email = data.get('email')
        if is_valid_email_regex.fullmatch(email):
            return super().validate(data)
        else:
            self.fail("email_mismatch")