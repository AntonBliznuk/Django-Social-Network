from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.view_post, name='view_post'),
    path('<int:post_id>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:user_id>/delete/post/', views.delete_post, name='delete_post'),
]