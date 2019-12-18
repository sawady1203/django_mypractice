# users/forms.py

"""
usernameを追加せずにemailとpasswordだけの認証にしたいが、それはdjango-allauthの設定で行う。
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()  # AUTH_USER_MODEL config in settings.py
        fields = ('email', 'username')  # password is default


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()  # AUTH_USER_MODEL config in settings.py
        fields = ('email', 'username')  # password is default
