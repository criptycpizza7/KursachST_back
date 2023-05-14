# Generated by Django 4.1.7 on 2023-05-13 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kursach_app', '0002_remove_company_country_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stocks',
            options={'get_latest_by': ['time'], 'verbose_name_plural': 'Stocks'},
        ),
        migrations.RenameField(
            model_name='stocks',
            old_name='change_percent',
            new_name='changePercent',
        ),
    ]
