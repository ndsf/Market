from django.urls import path
from . import views

app_name = 'information'
urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('update/', views.profile_update, name='profile_update'),
    path('detail/<username>/', views.user_detail, name='user_detail'),
    path('follow/', views.user_follow, name="user_follow"),
]
