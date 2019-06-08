from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index_url'),
    path('books/', views.BookListView.as_view(), name='books_url'),
    path('authors/', views.AuthorListView.as_view(), name='authors_url'),
    path('publishers/', views.PublisherListView.as_view(), name='publishers_url'),
    path('book/<str:slug>/', views.BookDetailView.as_view(), name='book_detail_url'),
    path('author/<str:id>/', views.AuthorDetailView.as_view(), name='author_detail_url'),
    path('publisher/<str:id>/', views.PublisherDetailView.as_view(), name='publisher_detail_url')
]