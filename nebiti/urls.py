from django.contrib.auth.views import LoginView
from django.urls import path
from .views import register, user_login, user_logout, home, create_post, cast_vote


# app_name = "nebiti"

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('create_post/', create_post, name='create_post'),
    path('cast-vote/<int:post_id>/<int:vote>/', cast_vote, name='cast_vote'),

    path('logout/', user_logout, name='logout'),



]
