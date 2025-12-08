from django.urls import path
from . import views

urlpatterns = [
    path("createPost", views.createPost),
    path("MyPost",views.mypost),
    path('update/<int:pid>/', views.post_update, name='post_update'),
    path('delete/<int:pid>/', views.post_delete, name='post_delete'),
    path('toggle-like/', views.toggle_like, name='toggle_like'),
    path("add-comment/", views.add_comment, name="add_comment"),
    path("<int:post_id>/comments/", views.get_comments, name="get_comments"),

]