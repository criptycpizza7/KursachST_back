# Generated by Django 4.1.7 on 2023-04-24 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kursach_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='country',
        ),
        migrations.RemoveField(
            model_name='company',
            name='number_of_shares',
        ),
        migrations.RemoveField(
            model_name='company',
            name='picture',
        ),
    ]
