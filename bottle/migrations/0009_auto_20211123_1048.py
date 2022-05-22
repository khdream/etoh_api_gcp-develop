# Generated by Django 3.2.9 on 2021-11-23 10:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bottle', '0008_remove_winecdc_denomination_wine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottlephoto',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='vintage',
            name='apogee',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='vintage',
            name='end_apogee',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='vintage',
            name='start_apogee',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='vintage',
            name='year',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='winemaker',
            name='creation_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
