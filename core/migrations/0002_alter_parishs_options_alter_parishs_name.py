# Generated by Django 5.0.6 on 2024-07-13 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parishs',
            options={'verbose_name': 'Parroquia'},
        ),
        migrations.AlterField(
            model_name='parishs',
            name='name',
            field=models.CharField(help_text='Nombre de la parroquia.', max_length=20, null=None, unique=True, verbose_name='nombre'),
        ),
    ]
