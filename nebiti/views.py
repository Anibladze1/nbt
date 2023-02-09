from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import RegisterForm, LoginForm, PostForm
from .models import Voter, Post, Vote


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Voter.objects.create(user=user, name=user.username)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'nebiti/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'nebiti/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    posts = Post.objects.all()
    return render(request, 'nebiti/home.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'nebiti/create_post.html', {'form': form})


@login_required
def cast_vote(request, post_id, vote):
    user = request.user
    try:
        voter = Voter.objects.get(user=user)
    except Voter.DoesNotExist:
        return redirect('home')
    post = Post.objects.get(id=post_id)
    vote_obj, created = Vote.objects.get_or_create(voter=voter, post=post)
    vote_obj.vote = vote
    vote_obj.save()
    return redirect('home')







