from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index_url'),
    path('books/', views.BookListView.as_view(), name='books_url'),
    path('authors/', views.AuthorListView.as_view(), name='authors_url'),
    path('publishers/', views.PublisherListView.as_view(), name='publishers_url'),
    path('genres/', views.GenreListView.as_view(), name='genres_url'),
    path('book/<str:slug>/', views.BookDetailView.as_view(), name='book_detail_url'),
    path('author/<str:id>/', views.AuthorDetailView.as_view(), name='author_detail_url'),
    path('publisher/<str:id>/', views.PublisherDetailView.as_view(), name='publisher_detail_url'),
    path('genre/<str:name>/', views.GenreDetailView.as_view(), name='genre_detail_url'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my_borrowed_url'),
    path('borrowed/', views.BorrowedBooksByUsersListView.as_view(), name='borrowed_all_url'),
    path('user_list/', views.UserListView.as_view(), name='users_url'),
    path('user/<str:username>', views.UserDetailView.as_view(), name='user_detail_url'),
]

urlpatterns += [
    path('book/<str:pk>/renew/', views.renew_bookinst, name='renew_bookinst_url'),
    path('authors/create/', views.AuthorCreate.as_view(), name='author_create_url'),
    path('author/<str:pk>/update', views.AuthorUpdate.as_view(), name='author_update_url'),
    path('author/<str:pk>/delete', views.AuthorDelete.as_view(), name='author_delete_url'),
]

urlpatterns += {
    path('genres/create/', views.GenreCreate.as_view(), name='genre_create_url'),
    path('genre/<str:pk>/update', views.GenreUpdate.as_view(), name='genre_update_url'),
    path('genre/<str:pk>/delete', views.GenreDelete.as_view(), name='genre_delete_url'),
}

urlpatterns += {
    path('publishers/create/', views.PublisherCreate.as_view(), name='publisher_create_url'),
    path('publisher/<str:pk>/update', views.PublisherUpdate.as_view(), name='publisher_update_url'),
    path('publisher/<str:pk>/delete', views.PublisherDelete.as_view(), name='publisher_delete_url'),
}

urlpatterns += [
    path('books/create/', views.BookCreate.as_view(), name='book_create_url'),
    path('book/<str:slug>/update', views.BookUpdate.as_view(), name='book_update_url'),
    path('book/<str:slug>/delete', views.BookDelete.as_view(), name='book_delete_url'),
]