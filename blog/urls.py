from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list_url'),
    path('tags/', views.TagList.as_view(), name='tag_list_url'),
    path('create/tag', views.TagCreate.as_view(), name='tag_create_url'),
    path('create/post', views.PostCreate.as_view(), name='post_create_url'),
    path('create/comment/', views.add_comment, name='add_comment_url'),
    path('update_comment/<str:pk>', views.CommentUpdate.as_view(), name='comment_update_url'),
    path('del_comment/<str:pk>', views.CommentDelete.as_view(), name='comment_delete_url'),
    path('post/<str:slug>/', views.PostDetail.as_view(), name='post_detail_url'),
    path('post/<str:slug>/update', views.PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/delete', views.PostDelete.as_view(), name='post_delete_url'),
    path('tag/<str:slug>/', views.TagDetail.as_view(), name='tag_detail_url'),

]
