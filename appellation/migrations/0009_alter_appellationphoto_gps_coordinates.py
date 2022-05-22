# Generated by Django 3.2.9 on 2021-11-25 12:55

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appellation', '0008_alter_appellationphoto_gps_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appellationphoto',
            name='gps_coordinates',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]
