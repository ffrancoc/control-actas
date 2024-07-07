# Generated by Django 5.0.6 on 2024-07-07 22:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_baptisms_identifier_alter_communions_baptism_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='baptisms',
            name='identifier',
            field=models.CharField(default='frQATxxo6yT9kPs', max_length=15, null=None),
        ),
        migrations.AlterField(
            model_name='books',
            name='identifier',
            field=models.CharField(max_length=50, null=None, unique=True),
        ),
        migrations.AlterField(
            model_name='communions',
            name='identifier',
            field=models.CharField(default='ek2bCH5BLHsVVh3', max_length=15, null=None),
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
    ]