from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("register", views.register, name="register"),
    path("memorylist", views.memoryList, name="memoryList"),
    path("newmemory", views.newMemory, name="newMemory"),
    path("fullscreen/<str:id>", views.memoryFullscreen, name="fullscreen"),
    path("delete", views.deleteMemory, name="deleteMemory"),
    path("random", views.random, name="random"),
]