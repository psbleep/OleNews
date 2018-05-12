from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Comment, Profile, NewsPost


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
        )
