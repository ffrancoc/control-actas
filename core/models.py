from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import shortuuid


class GenderChoices(models.TextChoices):
    MALE = 'Masculino', 'Masculino'
    FEMALE = 'Femenino', 'Femenino'


class TitleChoices(models.TextChoices):
    BAUTISMOS =  'Bautismos'
    COMUNIONES =  'Comuniones'
    CONFIRMACIONES =  'Confirmaciones'
    MATRIMONIOS =  'Matrimonios'


class PageChoices(models.IntegerChoices):
    PAGE_3 = 3, '3'
    PAGE_100 = 100, '100'
    PAGE_200 = 200, '200'
    PAGE_300 = 300, '300'
    PAGE_400 = 400, '400'
    PAGE_500 = 500, '500'
    
    

class Persons(models.Model):
        
    identifier = models.CharField(max_length=15, null=None, blank=False, unique=True, help_text='Identificador único de la persona generado automaticamente.')
    firstname = models.CharField(max_length=50, null=None, blank=False, help_text='Nombre completo de la persona.')
    lastname = models.CharField(max_length=50, null=None, blank=False, help_text='Apellido completo de la persona.')
    birthplace = models.CharField(max_length=50, null=None, blank=False, help_text='Lugar de nacimiento de la persona')
    birthday = models.DateField(null=None, blank=False, help_text='Fecha de nacimiento de la persona.')
    gender = models.CharField(max_length=9, null=None, blank=False, choices=GenderChoices.choices, default=GenderChoices.MALE, help_text='Genero de la persona.')

    father_info = models.CharField(max_length=80, null=None, blank=False, help_text='Nombre completo del padre de la persona.')
    mother_info = models.CharField(max_length=80, null=None, blank=False, help_text='Nombre completo de la madre de la persona.')

    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
    
class Parishs(models.Model):    
    
    name = models.CharField(max_length=20, null=None, blank=False, unique=True, help_text='Nombre de la parroquia.', verbose_name='nombre')
    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    
    def book_count(self):
        return Books.objects.filter(parish=self.pk).count()
    
    class Meta:
        verbose_name = 'Parroquia'
    

class Books(models.Model):

    title = models.CharField(max_length=14, null=None, blank=False, choices=TitleChoices.choices, default=TitleChoices.BAUTISMOS)
    parish = models.ForeignKey(Parishs, on_delete=models.RESTRICT)
    identifier = models.CharField(max_length=50, null=None, blank=False, unique=True, help_text='Identificador único del acta generado automaticamente.')
    description = models.CharField(max_length=50, null=None, blank=False, help_text='Descripción corta del libro, longitud max. 50 caracteres')
    n_pages = models.IntegerField(choices=PageChoices.choices, default=PageChoices.PAGE_100, help_text='Número de páginas o folios.')
    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
    def certificate_count(self):
        if self.title == TitleChoices.BAUTISMOS:
            return Baptisms.objects.filter(book=self.pk).count()
        else:
            return 0
    

class Baptisms(models.Model):

    book = models.ForeignKey(Books, on_delete=models.RESTRICT)    
    person = models.OneToOneField(Persons, null=False, on_delete=models.CASCADE)    
    
    baptism_date = models.DateField(null=None, blank=False, help_text='Fecha en la que se realizo la celebración.')
    priest = models.CharField(max_length=50, null=None, blank=False, help_text='Sacerdote que realizo la celebración.')
    parish_priest = models.CharField(max_length=50, null=None, blank=False, help_text='Sacerdote encargado de la parroquia.')

    godfather1_fullname = models.CharField(max_length=50, null=None, blank=False, help_text='Nombre completo del padrino o madrina del bautisado.')
    godfather2_fullname = models.CharField(max_length=50, null=True, blank=True, help_text='Nombre completo del segundo padrino o madrina del bautisado.')

    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
