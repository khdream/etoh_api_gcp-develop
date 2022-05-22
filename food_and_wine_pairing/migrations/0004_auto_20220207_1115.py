# Generated by Django 3.2.9 on 2022-02-07 11:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_and_wine_pairing', '0003_auto_20211210_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodwinematch',
            old_name='colour',
            new_name='color',
        ),
        migrations.RenameField(
            model_name='foodwinematch',
            old_name='denomination_wine',
            new_name='dvitivini',
        ),
        migrations.AddField(
            model_name='cooking',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='cooking',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='food',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='food',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='foodcategory',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='foodcategory',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='foodwinematch',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recipe',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recipe',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recipecooking',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recipecooking',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recipespice',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recipespice',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='spice',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='spice',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.RemoveField(
            model_name='food',
            name='category',
        ),
        migrations.AlterField(
            model_name='foodwinematch',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterModelTable(
            name='cooking',
            table='food_cooking',
        ),
        migrations.AlterModelTable(
            name='food',
            table='food_food',
        ),
        migrations.AlterModelTable(
            name='foodcategory',
            table='food_category',
        ),
        migrations.AlterModelTable(
            name='foodwinematch',
            table='food_wine_pairing',
        ),
        migrations.AlterModelTable(
            name='ingredient',
            table='food_ingredient',
        ),
        migrations.AlterModelTable(
            name='recipe',
            table='food_recipe',
        ),
        migrations.AlterModelTable(
            name='recipecooking',
            table='food_recipe_cooking',
        ),
        migrations.AlterModelTable(
            name='recipeingredient',
            table='food_recipe_ingredient',
        ),
        migrations.AlterModelTable(
            name='recipespice',
            table='food_recipe_spice',
        ),
        migrations.AlterModelTable(
            name='spice',
            table='food_spice',
        ),
        migrations.CreateModel(
            name='LinkFoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_categorie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipe_spices', to='food_and_wine_pairing.foodcategory')),
                ('id_mets', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipe_spices', to='food_and_wine_pairing.food')),
            ],
            options={
                'verbose_name': 'Recipe spice relation',
                'verbose_name_plural': 'Recipe spice relations',
                'db_table': 'food_link_food_category',
            },
        ),
        migrations.AddField(
            model_name='food',
            name='category',
            field=models.ManyToManyField(through='food_and_wine_pairing.LinkFoodCategory', to='food_and_wine_pairing.FoodCategory'),
        ),
    ]
