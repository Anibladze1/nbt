from django.contrib.auth.views import LoginView
from django.urls import path
from .views import register, create_post, home, login_view, like, dislike, logout_view, my_reactions


# app_name = "posts"

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('create_post/', create_post, name='create_post'),
    path('login/', login_view, name='login'),
    path('like/<int:pk>/', like, name='like'),
    path('dislike/<int:pk>/', dislike, name='dislike'),
    path('my-reactions/', my_reactions, name='my_reactions'),

    path('logout/', logout_view, name='logout'),



]
