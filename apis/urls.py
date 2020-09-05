from django.urls import path
from . import views
from .views import UserRegistration, CustomAuthToken, CreateBeach, UpdateBeach
from .beaches import create, update

urlpatterns = [
    path('register', UserRegistration.as_view()),
    path('u_token', CustomAuthToken.as_view()),
    path('create_beach', CreateBeach.as_view()),
    path('update_beach', UpdateBeach.as_view()),
    path('cr', create),
    path('u', update),
]
