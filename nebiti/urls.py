from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('create_post/', views.create_post, name='create_post'),
    path('cast-vote/<int:post_id>/<int:vote>/', views.cast_vote, name='cast_vote'),
    path('delegate/', views.delegate_vote, name='delegate'),
    path('my-votes/', views.my_votes, name='my_votes'),
    path('profile/', views.profile, name='profile'),

    path('logout/', views.user_logout, name='logout'),



]
