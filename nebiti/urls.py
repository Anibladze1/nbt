from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

# app_name = "nebiti"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('create_post/', views.create_post, name='create_post'),
    path('cast-vote/<int:post_id>/<int:vote>/', views.cast_vote, name='cast_vote'),
    path('delegate/', views.delegate_vote, name='delegate'),

    path('logout/', views.user_logout, name='logout'),



]
