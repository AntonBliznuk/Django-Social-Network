from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

"""
User registration form.
"""
class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
    

"""
User login form.
"""
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


"""
Form for uploading a new user photo.
"""
class UploadUserImage(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']


"""
Form for uploading a new user name.
"""
class UploadUserName(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

