from django.forms.models import ModelForm
from django.forms import ModelChoiceField, EmailField, CharField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms.widgets import Select, TextInput
from . import models


class UserUpdateForm(UserChangeForm):
    password = None
    email = EmailField(required=True, label='Email')    
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser')        
        widgets = {
            'first_name': TextInput(attrs={'required': 'required'}),
            'last_name': TextInput(attrs={'required': 'required'})
        }


class UserNewForm(UserCreationForm):    
    email = EmailField(required=True, label='Email')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'password1', 'password2')        
        widgets = {
            'first_name': TextInput(attrs={'required': 'required'}),
            'last_name': TextInput(attrs={'required': 'required'})
        }


class BookForm(ModelForm):
    class Meta:
        model = models.Books
        fields = ('title', 'identifier', 'description', 'n_pages')
        labels = {
            'title': 'Tipo de Libro',
            'identifier': 'Identificador',
            'description': 'Descripción (opcional)',
            'n_pages': 'Páginas',
        }
        widgets = {
            'title': Select(attrs={'class': 'form-control mb-2'}),
            'identifier': TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Ej. Parroquia Centro'}),
            'description': TextInput(attrs={'class': 'form-control mb-2'}),
            'n_pages': Select(attrs={'class': 'form-control mb-2'}),
        }


class BaptismForm(ModelForm):

    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.identifier

    def __init__(self, *args, **kwargs):
        super(BaptismForm, self).__init__(*args, **kwargs)
        self.fields['book'] = ModelChoiceField(queryset=models.Books.objects.filter(title=models.Books.TitleChoices.BAUTISMOS), widget=Select(attrs={'class': 'form-control mb-2'}))
        self.fields['book'].label = "Seleccionar Libro"        
        self.fields['book'].label_from_instance = self.label_from_instance

    class Meta:
        model = models.Baptisms
        fields = (
            'book',
            'firstname',
            'lastname',
            'birthplace',
            'birthday',
            'gender',
            'father_firstname',
            'father_lastname',
            'mother_firstname',
            'mother_lastname',
            'baptism_parish',
            'baptism_date',
            'priest',
            'parish_priest',
            'godfather1_fullname',
            'godfather2_fullname'
        )
        labels = {            
            'book': 'Seleccionar Libro',
            'firstname': 'Nombre Completo',
            'lastname': 'Apellido Completo',
            'birthplace': 'Lugar de Nacimiento',
            'birthday': 'Fecha de Nacimiento',
            'gender': 'Genero',
            'father_firstname': 'Nombre Completo del Padre',
            'father_lastname': 'Apellido Completo del Padre',
            'mother_firstname': 'Nombre Completo de la Madre',
            'mother_lastname': 'Apellido Completo de la Madre',
            'baptism_parish': 'Parroquia de Bautismo',
            'baptism_date': 'Fecha de Bautismo',
            'priest': 'Sacerdote',
            'parish_priest': 'Párroco',
            'godfather1_fullname': 'Nombres y Apellidos de Padrino 1',
            'godfather2_fullname': 'Nombres y Apellidos de Padrino 2 (opcional)'
        }
        widgets = {                   
            'firstname': TextInput(attrs={'class': 'form-control mb-2'}),
            'lastname': TextInput(attrs={'class': 'form-control mb-2'}),
            'birthplace': TextInput(attrs={'class': 'form-control mb-2'}),
            'birthday': TextInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-control mb-2'}),
            'father_firstname': TextInput(attrs={'class': 'form-control mb-2'}),
            'father_lastname': TextInput(attrs={'class': 'form-control mb-2'}),
            'mother_firstname': TextInput(attrs={'class': 'form-control mb-2'}),
            'mother_lastname': TextInput(attrs={'class': 'form-control mb-2'}),
            'baptism_parish': TextInput(attrs={'class': 'form-control mb-2'}),
            'baptism_date': TextInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
            'priest': TextInput(attrs={'class': 'form-control mb-2'}),
            'parish_priest': TextInput(attrs={'class': 'form-control mb-2'}),
            'godfather1_fullname': TextInput(attrs={'class': 'form-control mb-2'}),
            'godfather2_fullname': TextInput(attrs={'class': 'form-control mb-2'}),
        }