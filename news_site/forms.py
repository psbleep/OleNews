from django import forms
from .models import Comment, Profile, NewsPost
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm


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
        if 'parent_pk' in kwargs:
            parent_pk = kwargs.pop('parent_pk')
        else:
            parent_pk = None
        super().__init__(*args, **kwargs)
        self.fields['post'].initial = NewsPost.objects.get(pk=post_pk)
        self.fields['post'].widget = forms.HiddenInput()
        self.fields['user'].initial = User.objects.get(pk=user_pk)
        self.fields['user'].widget = forms.HiddenInput()
        if parent_pk is not None:
            print("Adding to Fields")
            self.fields['parent'].initial = Comment.objects.get(pk=parent_pk)
            self.fields['parent'].widget = forms.HiddenInput()

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
