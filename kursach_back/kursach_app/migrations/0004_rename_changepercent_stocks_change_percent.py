# Generated by Django 4.1.7 on 2023-05-13 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kursach_app', '0003_alter_stocks_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stocks',
            old_name='changePercent',
            new_name='change_percent',
        ),
    ]