# Generated by Django 5.0.6 on 2024-07-09 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_parishs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='description',
            field=models.CharField(help_text='Este campo debe ser representativo, ej. actas de bautismo parroquia san pedro. longitud max. 50 caracteres', max_length=50, null=None),
        ),
    ]
