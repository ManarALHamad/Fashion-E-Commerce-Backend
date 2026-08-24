from django.urls import path

from . import views


urlpatterns = [
    path("auth/sign-up", views.sign_up, name="sign-up"),
    path("auth/sign-in", views.sign_in, name="sign-in"),
    path("users", views.user_list, name="user-list"),
]
