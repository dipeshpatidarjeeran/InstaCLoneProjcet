from django.urls import path
from . import views

urlpatterns = [
    path("createPost", views.createPost),
    path("MyPost",views.mypost),
    path('update/<int:pid>/', views.post_update, name='post_update'),
    path('delete/<int:pid>/', views.post_delete, name='post_delete'),

]