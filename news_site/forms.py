from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from .models import NewsPost, Comment, Profile

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a '
                                                       'valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2',)

class LoginForm(AuthenticationForm):
    fields=('username','password')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class UserChange(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name'
        )
class UserChangeProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'user_bio',
        )
