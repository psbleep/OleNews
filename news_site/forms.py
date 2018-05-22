from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import Comment, Profile, NewsPost


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            ]

class LoginForm(AuthenticationForm):
    fields = ('username', 'password')


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        post_pk = kwargs.pop('post_pk')
        user_pk = kwargs.pop('user_pk')
        super().__init__(*args, **kwargs)
        self.fields['post'].initial = NewsPost.objects.get(pk=post_pk)
        self.fields['post'].widget = forms.HiddenInput()
        self.fields['user'].initial = User.objects.get(pk=user_pk)
        self.fields['user'].widget = forms.HiddenInput()

    class Meta:
        model = Comment
        fields = ('post', 'user', 'content')


class UserChange(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class UserChangeProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'user_bio',
            'email_consent',
            'avitar'
            )
