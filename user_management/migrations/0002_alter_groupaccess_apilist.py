# Generated by Django 3.2.9 on 2022-02-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupaccess',
            name='apiList',
            field=models.TextField(default=''),
        ),
    ]
