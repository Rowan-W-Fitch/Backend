from django.urls import path
from . import views
from .views import UserRegistration, CustomAuthToken, CreateBeach, UpdateBeach, RankBeaches, GetAllBeaches, CheckAuth

urlpatterns = [
    path('register', UserRegistration.as_view()),
    path('u_token', CustomAuthToken.as_view()),
    path('create_beach', CreateBeach.as_view()),
    path('update_beach', UpdateBeach.as_view()),
    path('get_spots', RankBeaches.as_view()),
    path('markers', GetAllBeaches.as_view()),
    path('check', CheckAuth.as_view()),
]
