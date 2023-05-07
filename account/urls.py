from django.urls import path
from .views import signup, close, users

urlpatterns = [
    path("signup", signup),
    path("users/<str:pk>", users),
    path("close", close)
]