# Generated by Django 3.2.9 on 2021-12-14 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0005_auto_20211210_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='grape',
            name='language_origin',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grape',
            name='name_english_alpahbet_latin',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grape',
            name='name_origin_alpahbet_latin',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grape',
            name='name_origin_alpahbet_origin',
            field=models.TextField(blank=True, null=True),
        ),
    ]