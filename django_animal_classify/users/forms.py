# users/forms.py

"""
usernameを追加せずにemailとpasswordだけの認証にしたいが、それはdjango-allauthの設定で行う。
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()  # AUTH_USER_MODEL config in settings.py
        fields = ('email', 'username')  # password is default


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()  # AUTH_USER_MODEL config in settings.py
        fields = ('email', 'username')  # password is default


class CustomSignupForm(SignupForm):
    age = forms.IntegerField()
    weight = forms.IntegerField()

    class Meta:
        model = get_user_model()

    def signup(self, request, user):
        user.age = self.cleaned_data['age']
        user.weight = self.cleaned_data['weight']
        user.save()
        return user
