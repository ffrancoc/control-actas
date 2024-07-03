
from django.urls import path

from . import views
from .view.baptism_view import BaptismView
from .view.book_view import BookView
from .view.communion_view import CommunionView
from .view.user_view import UserView

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_session, name='logout_session'),    
    path('index', views.index, name='index'),

    # Rutas para usuarios
    path('users', UserView.index, name='users'),    
    path('add/users', UserView.add, name='add_user'),    
]
