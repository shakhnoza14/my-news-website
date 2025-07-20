from django import forms
from .models import Usermodel, ProfileModel

class UserForm(forms.ModelForm):
    class Meta:
        model = Usermodel
        fields = ['username', 'password', 'email',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['user', 'bio', 'image', 'banner']

class EditModelForm(forms.ModelForm):
    username = forms.CharField(max_length=200)
    class Meta:
        model = ProfileModel
        fields = ['bio', 'image', 'username',]