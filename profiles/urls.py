from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('login/', views.login_page, name='login'),
    path('<int:user_id>/', views.profile_page, name='profile'),
    path('<int:user_id>/subscriptions/', views.user_subscriptions, name='subscriptions'),
    path('<int:user_id>/posts/', views.user_posts, name='posts'),
    path('<int:user_id>/delete/subscriptions/', views.delete_user_subscriptions, name='delete_user_subscriptions'),
]