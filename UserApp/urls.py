from django.urls import path
from . import views

urlpatterns = [
    path("login_user", views.login_user),
    path("logout", views.logout_user),
    path("register", views.Register),
    path("", views.homepage),
    path("profile", views.user_profile),
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path("edit_profile",views.edit_profile, name='edit_profile'),
    path('delete/<int:pid>/', views.post_delete, name='home_post_delete'),
    path('update/<int:pid>/', views.post_update, name='home_post_update'),
]