from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PostForm, LoginForm
from .models import Post, Reaction


def home(request):
    posts = Post.objects.all().order_by('-id')
    context = {'posts': posts}
    return render(request, 'nebiti/home.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'nebiti/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'nebiti/register.html', {'form': form})


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
def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        post=post
    )
    if not created:
        if reaction.reaction:
            messages.error(request, 'You have already liked this post.')
        else:
            reaction.reaction = True
            reaction.save()
            post.likes += 1
            post.dislikes -= 1
            post.save()
    else:
        reaction.reaction = True
        reaction.save()
        post.likes += 1
        post.save()
    return redirect('home')


@login_required
def dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        post=post
    )
    if not created:
        if not reaction.reaction:
            messages.error(request, 'You have already disliked this post.')
        else:
            reaction.reaction = False
            reaction.save()
            post.dislikes += 1
            post.likes -= 1
            post.save()
    else:
        reaction.reaction = False
        reaction.save()
        post.dislikes += 1
        post.save()
    return redirect('home')


@login_required
def my_reactions(request):
    reactions = Reaction.objects.filter(user=request.user)
    context = {'reactions': reactions}
    return render(request, 'nebiti/my-reactions.html', context)




