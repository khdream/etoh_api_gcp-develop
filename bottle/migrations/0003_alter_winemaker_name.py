# Generated by Django 3.2.9 on 2021-11-18 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bottle', '0002_remove_winecdc_list_denomination_wine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winemaker',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, unique=True),
        ),
    ]
