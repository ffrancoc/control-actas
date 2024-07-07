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
    PAGE_100 = 100, '100'
    PAGE_200 = 200, '200'
    PAGE_300 = 300, '300'
    PAGE_400 = 400, '400'
    PAGE_500 = 500, '500'
    
    

class Persons(models.Model):
        
    identifier = models.CharField(max_length=15, null=None, blank=False, unique=True)
    firstname = models.CharField(max_length=50, null=None, blank=False)
    lastname = models.CharField(max_length=50, null=None, blank=False)
    birthplace = models.CharField(max_length=50, null=None, blank=False)
    birthday = models.DateField(null=None, blank=False)
    gender = models.CharField(max_length=9, null=None, blank=False, choices=GenderChoices.choices, default=GenderChoices.MALE)

    father_info = models.CharField(max_length=80, null=None, blank=False)
    mother_info = models.CharField(max_length=80, null=None, blank=False)

    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
            
    

class Books(models.Model):

    title = models.CharField(max_length=14, null=None, blank=False, choices=TitleChoices.choices, default=TitleChoices.BAUTISMOS)
    identifier = models.CharField(max_length=50, null=None, blank=False, unique=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    n_pages = models.IntegerField(choices=PageChoices.choices, default=PageChoices.PAGE_100)
    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class Baptisms(models.Model):

    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=15, null=None, blank=False, default=shortuuid.ShortUUID().random(length=15))
    firstname = models.CharField(max_length=50, null=None, blank=False)
    lastname = models.CharField(max_length=50, null=None, blank=False)
    birthplace = models.CharField(max_length=50, null=None, blank=False)
    birthday = models.DateField(null=None, blank=False)
    gender = models.CharField(max_length=9, null=None, blank=False, choices=GenderChoices.choices, default=GenderChoices.MALE)

    father_info = models.CharField(max_length=80, null=None, blank=False)
    mother_info = models.CharField(max_length=80, null=None, blank=False)

    baptism_parish = models.CharField(max_length=50, null=None, blank=False)
    baptism_date = models.DateField(null=None, blank=False)
    priest = models.CharField(max_length=50, null=None, blank=False)
    parish_priest = models.CharField(max_length=50, null=None, blank=False)

    godfather1_fullname = models.CharField(max_length=50, null=None, blank=False)
    godfather2_fullname = models.CharField(max_length=50, null=True, blank=True)

    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)



class Communions(models.Model):    

    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    baptism = models.ForeignKey(Baptisms, null=True, blank=True,  on_delete=models.CASCADE)
    identifier = models.CharField(max_length=15, null=None, blank=False, default=shortuuid.ShortUUID().random(length=15))
    firstname = models.CharField(max_length=50, null=None, blank=False)
    lastname = models.CharField(max_length=50, null=None, blank=False)
    birthplace = models.CharField(max_length=50, null=None, blank=False)
    birthday = models.DateField(null=None, blank=False)
    gender = models.CharField(max_length=9, null=None, blank=False, choices=GenderChoices.choices, default=GenderChoices.MALE)

    father_info = models.CharField(max_length=80, null=None, blank=False)
    mother_info = models.CharField(max_length=80, null=None, blank=False)

    baptism_parish = models.CharField(max_length=50, null=None, blank=False)
    baptism_date = models.DateField(null=None, blank=False)

    communion_parish = models.CharField(max_length=50, null=None, blank=False)
    communion_date = models.DateField(null=None, blank=False)

    parish_priest = models.CharField(max_length=50, null=None, blank=False)

    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)