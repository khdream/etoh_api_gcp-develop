# Generated by Django 3.2.9 on 2021-11-25 14:37

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bottle', '0011_auto_20211124_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winemaker',
            name='gps_location',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]
