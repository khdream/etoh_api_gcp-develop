# Generated by Django 3.2.9 on 2021-11-23 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appellation', '0003_auto_20211123_1048'),
        ('core', '0003_alter_denominationwine_wine_cdc'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DenominationWine',
        ),
    ]
