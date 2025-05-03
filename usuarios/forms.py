from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_gerente', 'password1', 'password2']
