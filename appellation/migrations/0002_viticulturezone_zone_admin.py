# Generated by Django 3.2.9 on 2021-11-21 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appellation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='viticulturezone',
            name='zone_admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='viticulture_zone', to='appellation.adminzone'),
        ),
    ]
