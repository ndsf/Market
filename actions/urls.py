from django.urls import path
from . import views

app_name = 'actions'
urlpatterns = [
    path('create/', views.message_create, name='message_create'),
]