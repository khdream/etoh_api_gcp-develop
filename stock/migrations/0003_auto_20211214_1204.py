# Generated by Django 3.2.9 on 2021-12-14 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20211123_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottleprice',
            name='category',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottleprice',
            name='currency',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='bottleprice',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottleprice',
            name='promo_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scale',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity_available',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity_ordered',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity_reserved',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='alcohol',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='appellation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='certification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='colour',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='country',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='currency',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='grape_assemble',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='label',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='price_pre_taxe',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='price_with_taxe',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='ranking',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='region',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='sku',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='status',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='subregion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='vat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='vintage',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='volume',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='weight',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='wine_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='stocklist',
            name='winemaker',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
