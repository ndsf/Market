from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'article'
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('share/<int:id>/', views.post_share, name='post_share'),
    # path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('create/', views.post_create, name='post_create'),
    path('update/<int:id>/', views.post_update, name='post_update'),
    path('delete/<int:id>/', views.post_delete, name='post_delete'),
    path('like/', views.post_like, name='post_like'),
]
