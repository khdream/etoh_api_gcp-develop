# Generated by Django 3.2.9 on 2021-11-23 10:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20211123_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
