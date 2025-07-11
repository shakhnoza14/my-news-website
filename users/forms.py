from django import forms
from .models import Usermodel

class UserForm(forms.ModelForm):
    class Meta:
        model = Usermodel
        fields = ['username', 'password', 'email']