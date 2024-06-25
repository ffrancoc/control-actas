
from django.urls import path

from . import views
from .view.baptism_view import BaptismView
from .view.book_view import BookView
from .view.communion_view import CommunionView
from .view.user_view import UserView

urlpatterns = [
    path('logout', views.logout_session, name='logout_session'),
    path('home', views.home, name='home'),
    path('index', views.index, name='index'),
    # Rutas para usuarios
    path('users', UserView.index, name='users'),
    path('users/count', UserView.count, name='user_count'),
    path('users/list', UserView.users, name='user_list'),
    path('users/add', UserView.add, name='add_user'),
    path('users/<int:pk>/preview', UserView.preview, name='preview_user'),
    path('users/<int:pk>/edit', UserView.edit, name='edit_user'),
    path('users/<int:pk>/delete', UserView.delete, name='delete_user'),
    path('users/<int:pk>/password/', UserView.edit_password, name='edit_password'),
    # Rutas para buatismos
    path('baptisms', BaptismView.index, name='baptisms'),
    path('baptisms/count', BaptismView.count, name='baptism_count'),
    path('baptisms/list', BaptismView.baptisms, name='baptism_list'),
    path('baptisms/add', BaptismView.add, name='add_baptism'),
    path('baptisms/object', BaptismView.baptism_by_pk, name='baptism_object'),
    path('baptisms/<int:pk>/count', BaptismView.count_by_book, name='baptisms_count'),
    path('baptisms/<int:pk>/preview', BaptismView.preview, name='preview_baptism'),
    path('baptisms/<int:pk>/edit', BaptismView.edit, name='edit_baptism'),
    path('baptisms/<int:pk>/delete', BaptismView.delete, name='delete_baptism'),
    # Rutas para comuniones
    path('communions', CommunionView.index, name='communions'),
    path('communions/count', CommunionView.count, name='communion_count'),
    path('communions/list', CommunionView.communions, name='communion_list'),
    path('communions/add', CommunionView.add, name='add_communion'),
    path('communions/<int:pk>/count', CommunionView.count_by_book, name='communions_count'),
    # Rutas para Libros
    path('books', BookView.index, name='books'),
    path('books/count', BookView.count, name='book_count'),
    path('books/list', BookView.books, name='book_list'),
    path('books/add', BookView.add, name='add_book'),
    path('books/<int:pk>/edit', BookView.edit, name='edit_book'),    
    path('books/<int:pk>/delete', BookView.delete, name='delete_book'),
]
