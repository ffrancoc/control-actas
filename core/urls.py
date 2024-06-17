
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('baptisms', views.baptisms, name='baptisms'),
    path('baptisms/add', views.add_baptism, name='add_baptism'),
    path('baptisms/list', views.baptisms_list, name='baptism_list'),
    path('baptisms/<int:pk>/count', views.baptisms_count, name='baptisms_count'),
    path('baptisms/<int:pk>/preview', views.preview_baptism, name='preview_baptism'),
    path('baptisms/<int:pk>/edit', views.edit_baptism, name='edit_baptism'),
    path('baptisms/<int:pk>/delete', views.delete_baptism, name='delete_baptism'),
    path('books', views.books, name='books'),
    path('books/add', views.add_book, name='add_book'),
    path('books/list', views.book_list, name='book_list'),
    path('books/<int:pk>/edit', views.edit_book, name='edit_book'),    
    path('books/<int:pk>/delete', views.delete_book, name='delete_book'),
]
