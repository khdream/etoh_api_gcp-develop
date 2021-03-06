# Generated by Django 3.2.9 on 2021-12-09 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appellation', '0017_alter_appellation_sugar_dose'),
        ('core', '0004_delete_denominationwine'),
        ('bottle', '0016_alter_winecdclexicon_lexicon'),
        ('wine', '0003_auto_20211209_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grapeassembly',
            name='grape',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grape_assembles', to='wine.grape'),
        ),
        migrations.AlterField(
            model_name='winecdc',
            name='appellation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wine_cdc', to='appellation.appellation'),
        ),
        migrations.AlterField(
            model_name='winecdc',
            name='assemble',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wine_cdc', to='core.assemble'),
        ),
        migrations.AlterField(
            model_name='winecdc',
            name='wine_profile_cdc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wine_cdc', to='bottle.wineprofilecdc'),
        ),
    ]
