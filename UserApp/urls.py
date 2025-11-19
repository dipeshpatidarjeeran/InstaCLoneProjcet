from django.urls import path
from . import views

urlpatterns = [
    path("login_user", views.login_user),
    path("logout", views.logout_user),
    path("register", views.Register),
    path("", views.homepage),
    path("profile", views.profile),

]