# Generated by Django 5.0.6 on 2024-07-09 18:18

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Bautismos', 'Bautismos'), ('Comuniones', 'Comuniones'), ('Confirmaciones', 'Confirmaciones'), ('Matrimonios', 'Matrimonios')], default='Bautismos', max_length=14, null=None)),
                ('identifier', models.CharField(max_length=50, null=None, unique=True)),
                ('description', models.CharField(help_text='Este campo debe ser representativo, ej. actas de bautismo parroquia san pedro. longitud max. 80 caracteres', max_length=80, null=None)),
                ('n_pages', models.IntegerField(choices=[(100, '100'), (200, '200'), (300, '300'), (400, '400'), (500, '500')], default=100)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, null=None)),
                ('modified', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=15, null=None, unique=True)),
                ('firstname', models.CharField(max_length=50, null=None)),
                ('lastname', models.CharField(max_length=50, null=None)),
                ('birthplace', models.CharField(max_length=50, null=None)),
                ('birthday', models.DateField(null=None)),
                ('gender', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], default='Masculino', max_length=9, null=None)),
                ('father_info', models.CharField(max_length=80, null=None)),
                ('mother_info', models.CharField(max_length=80, null=None)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, null=None)),
                ('modified', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Baptisms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baptism_parish', models.CharField(max_length=50, null=None)),
                ('baptism_date', models.DateField(null=None)),
                ('priest', models.CharField(max_length=50, null=None)),
                ('parish_priest', models.CharField(max_length=50, null=None)),
                ('godfather1_fullname', models.CharField(max_length=50, null=None)),
                ('godfather2_fullname', models.CharField(blank=True, max_length=50, null=True)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, null=None)),
                ('modified', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.books')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.persons')),
            ],
        ),
    ]
