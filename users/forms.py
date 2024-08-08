from django import forms

from .models import UserAccount

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ('full_name','username', 'email', 'avatar',)