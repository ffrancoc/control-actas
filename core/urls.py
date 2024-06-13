
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('books', views.books, name='books'),
    path('books/list', views.book_List, name='book_list'),
    path('books/add', views.add_book, name='add_book'),
    path('books/<int:pk>/edit', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete', views.delete_book, name='delete_book'),
]
