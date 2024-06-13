from django.forms.models import ModelForm
from django.forms.widgets import Select, TextInput
from django.forms import fields
from . import models



class BookForm(ModelForm):
    class Meta:
        model = models.Books
        fields = ('title', 'description', 'n_pages')
        labels = {
            'title': 'Tipo de Libro',
            'description': 'Descripción (opcional)',
            'n_pages': 'Páginas',
        }
        widgets = {
            'title': Select(attrs={'class': 'form-control mb-2'}),
            'description': TextInput(attrs={'class': 'form-control mb-2'}),
            'n_pages': Select(attrs={'class': 'form-control mb-2'}),
        }


class EditBookForm(ModelForm):
    
    class Meta:
        model = models.Books
        fields = ('title', 'description', 'n_pages')
        labels = {
            'title': 'Tipo de Libro',
            'description': 'Descripción (opcional)',
            'n_pages': 'Páginas',
        }
        widgets = {
            'title': Select(attrs={'class': 'form-control mb-2', 'disabled': 'disabled'}),
            'description': TextInput(attrs={'class': 'form-control mb-2'}),
            'n_pages': Select(attrs={'class': 'form-control mb-2', 'disabled': 'disabled'}),
        }