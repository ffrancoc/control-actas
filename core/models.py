from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Books(models.Model):

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

    title = models.CharField(max_length=14, null=None, blank=False, choices=TitleChoices.choices, default=TitleChoices.BAUTISMOS)
    description = models.CharField(max_length=50, null=True, blank=True, help_text='El número de carácteres máximo es de 50')
    n_pages = models.IntegerField(choices=PageChoices.choices, default=PageChoices.PAGE_100)
    create_at = models.DateTimeField(null=None, blank=False, default=timezone.now)
    modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)