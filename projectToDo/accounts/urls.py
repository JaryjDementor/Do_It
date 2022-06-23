from django.urls import path
from .views import (
    login_request,
    register_request,
    logout_request,
    firstpage,
)

urlpatterns = [
    path("", firstpage, name="firstpage"),
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path("logout", logout_request, name="logout"),
]
