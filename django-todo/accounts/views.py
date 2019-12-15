# accounts/views.py

# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm  # 変更
    success_url = reverse_lazy('login')  # redirectさせる
    template_name = 'accounts/signup.html'
