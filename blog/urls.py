from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list_url'),
    path('create/', views.PostCreate.as_view(), name='post_create_url'),
    path('post/<str:slug>/', views.PostDetail.as_view(), name='post_detail_url'),
    path('post/<str:slug>/update', views.PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/delete', views.PostDelete.as_view(), name='post_delete_url'),
    path('tag/<str:slug>/', views.TagDetail.as_view(), name='tag_detail_url'),
]
