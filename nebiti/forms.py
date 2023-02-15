from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Voter


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='პაროლი', widget=forms.PasswordInput)
    password2 = forms.CharField(label='გაიმეორეთ პაროლი', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'სახელი',
            'last_name': 'გვარი',
            'email': 'ელ-ფოსტა',
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='პაროლი', widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        labels = {
            'title': 'სათაური',
            'description': 'ტექსტი',
        }


class DelegateVoteForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['delegate']
        labels = {
            'delegate': 'დელეგატი',
        }

