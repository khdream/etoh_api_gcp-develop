# Generated by Django 3.2.9 on 2022-02-07 11:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0006_alphabet_country_language'),
        ('appellation', '0021_auto_20220207_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgingDefault',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_productspec', models.BigIntegerField(blank=True, null=True)),
                ('type_aging', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Aging',
                'verbose_name_plural': 'Agings',
            },
        ),
        migrations.CreateModel(
            name='Aroma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Aroma',
                'verbose_name_plural': 'Aromas',
            },
        ),
        migrations.CreateModel(
            name='Assemble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'productspec_blend',
            },
        ),
        migrations.CreateModel(
            name='CategoryLexicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Lexicon Category',
                'verbose_name_plural': 'Lexicon Categories',
                'db_table': 'productspec_glossarycategory',
            },
        ),
        migrations.CreateModel(
            name='DenominationWine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Denomination Wine',
                'verbose_name_plural': 'Denominations Wine',
                'db_table': 'productspec_dvitivini',
            },
        ),
        migrations.CreateModel(
            name='Grape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('color_varietal', models.CharField(blank=True, max_length=255, null=True)),
                ('technical_name', models.TextField(blank=True, null=True)),
                ('survey_hectares', models.TextField(blank=True, null=True)),
                ('date_servey_hectares', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('comment_varietal', models.TextField(blank=True, null=True)),
                ('aromas', models.TextField(blank=True, null=True)),
                ('description_taste', models.TextField(blank=True, null=True)),
                ('description_visual', models.TextField(blank=True, null=True)),
                ('skins', models.TextField(blank=True, null=True)),
                ('cultural_aptitudes', models.TextField(blank=True, null=True)),
                ('phenology', models.TextField(blank=True, null=True)),
                ('susceptibility_diseases', models.TextField(blank=True, null=True)),
                ('guard_potential', models.TextField(blank=True, null=True)),
                ('yields', models.TextField(blank=True, null=True)),
                ('maturity', models.TextField(blank=True, null=True)),
                ('berry_size', models.TextField(blank=True, null=True)),
                ('type_variety', models.TextField(blank=True, null=True)),
                ('species', models.TextField(blank=True, null=True)),
                ('clones', models.TextField(blank=True, null=True)),
                ('year_cross', models.TextField(blank=True, null=True)),
                ('creator', models.TextField(blank=True, null=True)),
                ('name_origin_alphabet_origin', models.TextField(blank=True, null=True)),
                ('name_origin_alphabet_latin', models.TextField(blank=True, null=True)),
                ('name_en', models.TextField(blank=True, null=True)),
                ('language_origin', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('origin_country_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.country')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='productspec.grape')),
            ],
            options={
                'verbose_name': 'Grape',
                'verbose_name_plural': 'Grapes',
                'db_table': 'productspec_varietal',
            },
        ),
        migrations.CreateModel(
            name='GrapeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taste_acidity', models.IntegerField(blank=True, null=True)),
                ('taste_alcohol', models.IntegerField(blank=True, null=True)),
                ('taste_body', models.IntegerField(blank=True, null=True)),
                ('arom_complexity', models.IntegerField(blank=True, null=True)),
                ('arom_intensity', models.IntegerField(blank=True, null=True)),
                ('arom_length', models.IntegerField(blank=True, null=True)),
                ('note_general', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Lexicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('source', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lexicons', to='productspec.categorylexicon')),
            ],
            options={
                'verbose_name': 'Lexicon',
                'verbose_name_plural': 'Lexicons',
                'db_table': 'productspec_glossary',
            },
        ),
        migrations.CreateModel(
            name='Robe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(blank=True, max_length=255, null=True)),
                ('color_value', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Robe',
                'verbose_name_plural': 'Robes',
                'db_table': 'productspec_color',
            },
        ),
        migrations.CreateModel(
            name='SugarDose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('type_product', models.TextField(blank=True, null=True)),
                ('sweetness_min', models.FloatField(blank=True, null=True)),
                ('sweetness_max', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Dose',
                'verbose_name_plural': 'Doses',
                'db_table': 'productspec_dosagesweetness',
            },
        ),
        migrations.CreateModel(
            name='WineCDC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('color', models.TextField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('list_dvitivini', models.TextField(blank=True, null=True)),
                ('comment_descritpion', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_app', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wine_cdc', to='appellation.appellation')),
                ('id_blend_default', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wine_cdc', to='productspec.assemble')),
                ('sugar_dose_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wine_cdc', to='productspec.sugardose')),
            ],
            options={
                'verbose_name': 'Wine CDC',
                'verbose_name_plural': 'Wine CDCs',
                'db_table': 'productspec_productspec',
            },
        ),
        migrations.CreateModel(
            name='WineProfileCDC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taste_acidity', models.IntegerField(blank=True, null=True)),
                ('taste_alcohol', models.IntegerField(blank=True, null=True)),
                ('taste_body', models.IntegerField(blank=True, null=True)),
                ('taste_sweetness', models.IntegerField(blank=True, null=True)),
                ('arom_complexity', models.IntegerField(blank=True, null=True)),
                ('arom_intensity', models.IntegerField(blank=True, null=True)),
                ('arom_length', models.IntegerField(blank=True, null=True)),
                ('note_general', models.TextField(blank=True, null=True)),
                ('color_desc', models.TextField(blank=True, null=True)),
                ('note_fruity', models.TextField(blank=True, null=True)),
                ('note_acidity', models.TextField(blank=True, null=True)),
                ('note_body', models.TextField(blank=True, null=True)),
                ('note_intensity', models.TextField(blank=True, null=True)),
                ('temperature', models.TextField(blank=True, null=True)),
                ('opening_time', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('color_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wine_profile_cdc', to='productspec.robe')),
            ],
            options={
                'verbose_name': 'WineProfileCDC',
                'verbose_name_plural': 'WineProfileCDCs',
                'db_table': 'productspec_profile',
            },
        ),
        migrations.CreateModel(
            name='WineCDCLexicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coeff', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_glossary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wine_cdc_lexicons', to='productspec.lexicon')),
                ('id_productspec', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wine_cdc_lexicons', to='productspec.winecdc')),
            ],
            options={
                'verbose_name': 'WineCDCLexicon',
                'verbose_name_plural': 'WineCDCLexicons',
                'db_table': 'productspec_link_wine_glossary',
            },
        ),
        migrations.CreateModel(
            name='WineCDCDvitivini',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_dvitivini', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winecdc_dvitivini', to='productspec.denominationwine')),
                ('id_productspec', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winecdc_dvitivini', to='productspec.winecdc')),
            ],
            options={
                'db_table': 'productspec_link_wine_dvitivini',
            },
        ),
        migrations.AddField(
            model_name='winecdc',
            name='wine_profile_cdc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wine_cdc', to='productspec.wineprofilecdc'),
        ),
        migrations.CreateModel(
            name='Vintage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apogee_min', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('apogee', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('apogee_max', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('quality', models.FloatField(blank=True, null=True)),
                ('year', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('comment_vintage', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_productspec', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vintages', to='productspec.winecdc')),
            ],
            options={
                'verbose_name': 'Vintage',
                'verbose_name_plural': 'Vintages',
            },
        ),
        migrations.CreateModel(
            name='PlantationVarietal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_varietal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plantation_varietal', to='productspec.grape')),
                ('id_zviti', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plantation_varietal', to='appellation.viticulturezone')),
            ],
            options={
                'db_table': 'productspec_plantation_varietal',
            },
        ),
        migrations.CreateModel(
            name='LinkGlossaryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_categorie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='glossary_category', to='productspec.categorylexicon')),
                ('id_lexique', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='glossary_category', to='productspec.lexicon')),
            ],
            options={
                'db_table': 'productspec_linkglossarycategory',
            },
        ),
        migrations.CreateModel(
            name='GrapeSyn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='varietal_syn', to='productspec.grape')),
            ],
            options={
                'db_table': 'productspec_varietal_syn',
            },
        ),
        migrations.CreateModel(
            name='GrapeParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_child', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='varietal_parent_child', to='productspec.grape')),
                ('id_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='varietal_parent_parent', to='productspec.grape')),
            ],
            options={
                'db_table': 'productspec_varietalparent',
            },
        ),
        migrations.CreateModel(
            name='GrapeMainAccessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_accessory', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('grape', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grape_main_accessory', to='productspec.grape')),
                ('wine_cdc_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='varietal_main_accessory', to='productspec.winecdc')),
            ],
            options={
                'db_table': 'productspec_varietal_main_accessory',
            },
        ),
        migrations.CreateModel(
            name='GrapeAssembly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.IntegerField(blank=True, null=True)),
                ('main_accessory', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('assemble', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grape_assemble', to='productspec.assemble')),
                ('grape', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grape_assembles', to='productspec.grape')),
            ],
            options={
                'db_table': 'productspec_varietal_blend',
            },
        ),
        migrations.AddField(
            model_name='grape',
            name='varietal_profile_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grapes', to='productspec.grapeprofile'),
        ),
        migrations.AddField(
            model_name='denominationwine',
            name='wine_cdc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='denomination_wine', to='productspec.winecdc'),
        ),
        migrations.CreateModel(
            name='AromaProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_aroma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aroma_profile', to='productspec.aroma')),
                ('id_profile_vin_spec', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aroma_profile', to='productspec.winecdc')),
            ],
            options={
                'db_table': 'productspec_link_aroma_profile',
            },
        ),
        migrations.AddField(
            model_name='aroma',
            name='profile_wine_cdc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aromas', to='productspec.wineprofilecdc'),
        ),
    ]
