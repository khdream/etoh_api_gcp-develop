# Generated by Django 3.2.9 on 2021-11-22 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bottle', '0008_remove_winecdc_denomination_wine'),
        ('core', '0002_denominationwine_wine_cdc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denominationwine',
            name='wine_cdc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='denomination_wine', to='bottle.winecdc'),
        ),
    ]
