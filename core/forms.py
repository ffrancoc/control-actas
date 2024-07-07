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
            'father_info': 'Información Completa del Padre', 
            'mother_info': 'Información Completa de la Madre'
        }
        widgets = {
            'identifier': TextInput(attrs={'class': 'form-control mb-2', 'readonly': True}),
            'firstname': TextInput(attrs={'class': 'form-control mb-2'}),
            'lastname': TextInput(attrs={'class': 'form-control mb-2'}),
            'birthplace': TextInput(attrs={'class': 'form-control mb-2'}),
            'birthday': TextInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-control mb-2'}), 
            'father_info': TextInput(attrs={'class': 'form-control mb-2'}),
            'mother_info': TextInput(attrs={'class': 'form-control mb-2'})
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
            'title': Select(attrs={'class': 'form-control mb-2'}),
            'identifier': TextInput(attrs={'class': 'form-control mb-2', 'readonly': True}),
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
            'father_info',                        
            'mother_info',
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
            'father_info': 'Información del Padre',            
            'mother_info': 'Información de la Madre',
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
            'father_info': TextInput(attrs={'class': 'form-control mb-2'}),            
            'mother_info': TextInput(attrs={'class': 'form-control mb-2'}),
            'baptism_parish': TextInput(attrs={'class': 'form-control mb-2'}),
            'baptism_date': TextInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
            'priest': TextInput(attrs={'class': 'form-control mb-2'}),
            'parish_priest': TextInput(attrs={'class': 'form-control mb-2'}),
            'godfather1_fullname': TextInput(attrs={'class': 'form-control mb-2'}),
            'godfather2_fullname': TextInput(attrs={'class': 'form-control mb-2'}),
        }



class CommunionForm(ModelForm):

    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.identifier
    

    @staticmethod
    def label_from_baptism_instance(obj):
        return "%s" % obj.identifier
    

    def __init__(self, *args, **kwargs):
        super(CommunionForm, self).__init__(*args, **kwargs)
        self.fields['book'] = ModelChoiceField(queryset=models.Books.objects.filter(title=models.Books.TitleChoices.COMUNIONES), widget=Select(attrs={'class': 'form-control mb-2'}))
        self.fields['book'].label = "Seleccionar Libro"        
        self.fields['book'].label_from_instance = self.label_from_instance

        self.fields['baptism'] = ModelChoiceField(queryset=models.Baptisms.objects.all(), required=False, widget=Select(attrs={            
            'class': 'form-control mb-2', 
            'onchange': 'onChangeBaptism()',
            'hx-trigger': 'change', 
            'hx-get': f'{reverse("baptism_object")}',           
            'hx-include': '[name="baptism"]',
            'hx-target': '#content'
            }))
        self.fields['baptism'].label = "Id. Bautismo (opcional)"        
        self.fields['baptism'].label_from_instance = self.label_from_baptism_instance
        

    class Meta:
        model = models.Communions
        fields = (
            'book',
            'baptism',
            'firstname',
            'lastname',
            'birthplace',
            'birthday',
            'gender',
            'father_info',            
            'mother_info',
            'baptism_parish',
            'baptism_date',
            'communion_parish',
            'communion_date',
            'parish_priest'            
        )
        labels = {            
            'book': 'Seleccionar Libro',
            'baptism': 'Seleccionar Bautismo',
            'firstname': 'Nombre Completo',
            'lastname': 'Apellido Completo',
            'birthplace': 'Lugar de Nacimiento',
            'birthday': 'Fecha de Nacimiento',
            'gender': 'Genero',
            'father_info': 'Información del Padre',            
            'mother_info': 'Información de la Madre',
            'baptism_parish': 'Parroquia de Bautismo',
            'baptism_date': 'Fecha de Bautismo',
            'communion_parish': 'Parroquia de Comunión',
            'communion_date': 'Fecha de Comunión',
            'parish_priest': 'Párroco'
        }            
        widgets = {                               
            'firstname': TextInput(attrs={'class': 'form-control mb-2'}),
            'lastname': TextInput(attrs={'class': 'form-control mb-2'}),
            'birthplace': TextInput(attrs={'class': 'form-control mb-2'}),
            'birthday': TextInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-control mb-2'}),
            'father_info': TextInput(attrs={'class': 'form-control mb-2'}),            
            'mother_info': TextInput(attrs={'class': 'form-control mb-2'}),
            'baptism_parish': TextInput(attrs={'class': 'form-control mb-2'}),
            'baptism_date': TextInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
            'communion_parish': TextInput(attrs={'class': 'form-control mb-2'}),
            'communion_date': TextInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
            'parish_priest': TextInput(attrs={'class': 'form-control mb-2'}),            
        }