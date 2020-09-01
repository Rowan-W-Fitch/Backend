from django.urls import path
from . import views
from .views import UserRegistration, CustomAuthToken

urlpatterns = [
    path('register', UserRegistration.as_view()),
    path('u_token', CustomAuthToken.as_view()),
]
