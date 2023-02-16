from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, LoginForm, PostForm, DelegateVoteForm
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


# this is the view for the vote
@login_required()
def cast_vote(request, post_id, vote):
    user = request.user
    try:
        voter = Voter.objects.get(user=user)
    except Voter.DoesNotExist:
        return redirect('home')

    post = Post.objects.get(id=post_id)

    Vote.objects.update_or_create(voter=voter, post=post, defaults={'vote': vote})

    delegates_to_vote = list(voter.delegate.all())
    while delegates_to_vote:
        delegate = delegates_to_vote.pop()
        if delegate:
            Vote.objects.update_or_create(voter=delegate, post=post, defaults={'vote': vote})
            delegates_to_vote.extend(list(delegate.delegate.all()))

    return redirect('home')



# this is the view for the delegate vote form
@login_required()
def delegate_vote(request):
    if request.method == 'POST':
        form = DelegateVoteForm(request.POST)
        if form.is_valid():
            delegate_to = form.cleaned_data['delegated_to']
            user = request.user
            try:
                voter = Voter.objects.get(user=user)
                voter.delegated_to = delegate_to
                voter.save()
                return redirect('home')
            except Voter.DoesNotExist:
                return redirect('home')
    else:
        user_list = User.objects.all()
        form = DelegateVoteForm(initial={'delegated_to': user_list})
    return render(request, 'nebiti/delegate_vote.html', {'form': form})


# this is the view for my votes
@login_required
def my_votes(request):
    user_votes = Vote.objects.filter(voter=request.user.voter)
    delegated_votes = Vote.objects.filter(voter__delegate=request.user.voter)
    return render(request, 'nebiti/my-votes.html', {'user_votes': user_votes, 'delegated_votes': delegated_votes})


# this is the view for the profile
@login_required
def profile(request):
    return render(request, 'nebiti/profile.html')
