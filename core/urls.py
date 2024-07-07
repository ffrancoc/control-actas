
from django.urls import path

from . import views
from .view.baptism_view import BaptismView
from .view.book_view import BookView
from .view.communion_view import CommunionView
from .view.user_view import UserView
from .view.person_view import PersonView

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_session, name='logout_session'),    
    path('index', views.index, name='index'),

    # Rutas para usuarios
    path('users', UserView.index, name='users'),    
    path('add/users', UserView.add, name='add_user'),    
    path('delete/users', UserView.delete, name='delete_user'),  
    path('get/<int:pk>/users', UserView.user, name='get_user'),    
    path('edit/<int:pk>/users', UserView.edit, name='edit_user'),    
    path('edit/password/<int:pk>/users', UserView.edit_password, name='edit_user_password'),
    path('group/<int:pk>/users', UserView.group, name='group_user'),    

    # Rutas para personas
    path('persons', PersonView.index, name='persons'),    
    path('add/persons', PersonView.add, name='add_person'),    
    path('delete/persons', PersonView.delete, name='delete_person'),  
    path('get/<int:pk>/persons', PersonView.person, name='get_person'),    
    path('edit/<int:pk>/persons', PersonView.edit, name='edit_person'), 

    # Rutas para los libros
    path('books', BookView.index, name='books'),    
    path('add/books', BookView.add, name='add_book'),    
    path('delete/books', BookView.delete, name='delete_book'),  
    path('edit/<int:pk>/books', BookView.edit, name='edit_book'),   
]
