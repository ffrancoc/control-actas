from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
                                       UserCreationForm)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms import CharField, EmailField, ModelChoiceField
from django.forms.models import ModelForm
from django.forms.widgets import Select, TextInput
from django.urls import reverse

from . import models


class UserUpdateForm(UserChangeForm):
    password = None
    email = EmailField(required=True, label='Email')    
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups', 'is_active')        
        widgets = {
            # 'first_name': TextInput(attrs={'required': 'required'}),
            # 'last_name': TextInput(attrs={'required': 'required'})
        }


class UserNewForm(UserCreationForm):    
    email = EmailField(required=True, label='Email')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups', 'password1', 'password2')        
        widgets = {
            # 'first_name': TextInput(attrs={'required': 'required'}),
            # 'last_name': TextInput(attrs={'required': 'required'})
        }


class PersonForm(ModelForm):
    class Meta:
        model = models.Persons
        fields = ('identifier', 'firstname', 'lastname', 'birthplace',  'birthday', 'gender', 'father_info', 'mother_info')
        labels = {
            'identifier': 'Identificador', 
            'firstname': 'Nombre Completo', 
            'lastname': 'Apellido Completo', 
            'birthplace': 'Lugar de Nacimiento',            
            'birthday': 'Fecha de Nacimiento',
            'gender': 'Genero', 
            'father_info': 'Información del Padre', 
            'mother_info': 'Información de la Madre'
        }
        widgets = {
            'identifier': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'firstname': TextInput(attrs={'class': 'form-control'}),
            'lastname': TextInput(attrs={'class': 'form-control'}),
            'birthplace': TextInput(attrs={'class': 'form-control'}),
            'birthday': TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-control'}), 
            'father_info': TextInput(attrs={'class': 'form-control'}),
            'mother_info': TextInput(attrs={'class': 'form-control'})
        }

class ParishForm(ModelForm):
    class Meta:
        model = models.Parishs
        fields = ('name',)
        labels = {
            'name': 'Parroquia'
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'})
        }

class BookForm(ModelForm):
    class Meta:
        model = models.Books
        fields = ('title', 'identifier', 'description', 'n_pages')
        labels = {
            'title': 'Tipo de Libro',
            'identifier': 'Identificador',
            'description': 'Descripción',
            'n_pages': 'Páginas',
        }
        widgets = {
            'title': Select(attrs={'class': 'form-control'}),
            'identifier': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'n_pages': Select(attrs={'class': 'form-control'}),
        }


class BaptismForm(ModelForm):

    @staticmethod
    def label_from_book_instance(obj):
        return "%s - %s" % (obj.identifier, obj.description)
    
    @staticmethod
    def label_from_person_instance(obj):
        return "%s %s" % (obj.firstname, obj.lastname)
    
    @staticmethod
    def label_from_baptism_parish_instance(obj):
        return "%s" % obj.name
    

    def __init__(self, *args, **kwargs):
        super(BaptismForm, self).__init__(*args, **kwargs)
        self.fields['book'] = ModelChoiceField(queryset=models.Books.objects.filter(title=models.TitleChoices.BAUTISMOS), widget=Select(attrs={'class': 'form-control'}))
        self.fields['book'].label = "Libro"        
        self.fields['book'].label_from_instance = self.label_from_book_instance
        
        self.fields['person'] = ModelChoiceField(queryset=models.Persons.objects.all(), widget=Select(attrs={'class': 'form-control'}))
        self.fields['person'].label = "Persona"        
        self.fields['person'].label_from_instance = self.label_from_person_instance
        
        self.fields['baptism_parish'] = ModelChoiceField(queryset=models.Parishs.objects.all(), widget=Select(attrs={'class': 'form-control'}))
        self.fields['baptism_parish'].label = "Parroquia"        
        self.fields['baptism_parish'].label_from_instance = self.label_from_baptism_parish_instance
        

    class Meta:
        model = models.Baptisms
        fields = (
            'book',
            'person',            
            'baptism_parish',
            'baptism_date',
            'priest',
            'parish_priest',
            'godfather1_fullname',
            'godfather2_fullname'
        )
        labels = {                        
            'baptism_parish': 'Parroquia',
            'baptism_date': 'Fecha',
            'priest': 'Sacerdote',
            'parish_priest': 'Párroco',
            'godfather1_fullname': 'Padrino o Madrina 1',
            'godfather2_fullname': 'Padrino o Madrina 2'
        }
        widgets = {                               
            'baptism_parish': TextInput(attrs={'class': 'form-control'}),
            'baptism_date': TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priest': TextInput(attrs={'class': 'form-control'}),
            'parish_priest': TextInput(attrs={'class': 'form-control '}),
            'godfather1_fullname': TextInput(attrs={'class': 'form-control'}),
            'godfather2_fullname': TextInput(attrs={'class': 'form-control'}),
        }

