from django.urls import path
from . import views

app_name = 'actions'
urlpatterns = [
    path('create/', views.message_create, name='message_create'),
    path('conversation/<int:id>', views.conversation, name='conversation'),
    path('delete/<int:id>/', views.message_delete, name='message_delete'),
]