# Generated by Django 3.2.9 on 2021-12-10 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bottle', '0016_alter_winecdclexicon_lexicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agingdefault',
            name='type_aging',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aroma',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='aroma',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bottle',
            name='code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='bottle',
            name='container',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottle',
            name='gtin',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottle',
            name='volume',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottlephoto',
            name='definition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottlephoto',
            name='file_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottlephoto',
            name='media_photo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottlephoto',
            name='shooting',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottlephoto',
            name='source',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottlephoto',
            name='type_photo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bottlephoto',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categorylexicon',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lexicon',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lexicon',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lexicon',
            name='source',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='noteguide',
            name='guide',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='noteguide',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='robe',
            name='name_colour',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='robe',
            name='value_colour',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vintage',
            name='comment_vintage',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vintage',
            name='quality',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winebottle',
            name='alcohol',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winebottle',
            name='certification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winebottle',
            name='comment_degustation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winebottle',
            name='comment_vinification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winebottle',
            name='comment_viticulture',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winebottle',
            name='name_tank',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winecdclexicon',
            name='coefficient',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemaker',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemaker',
            name='comment_winemaker',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemaker',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='winemaker',
            name='siren',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemaker',
            name='type_winemaker',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemaker',
            name='viticulture',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemaker',
            name='winemaker_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winemakers', to='bottle.winemakerprofile'),
        ),
        migrations.AlterField(
            model_name='winemakerprofile',
            name='acidity_taste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemakerprofile',
            name='alcohol_taste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemakerprofile',
            name='aroma_complexity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemakerprofile',
            name='aroma_intensity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemakerprofile',
            name='aroma_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemakerprofile',
            name='body_taste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemakerprofile',
            name='general_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='winemakerprofile',
            name='sucrosite_taste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='acidity_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='acidity_taste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='alcohol_taste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='aroma_complexity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='aroma_intensity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='aroma_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='body_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='body_taste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='fruity_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='general_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='intensity_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='opening_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='robe_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wineprofilecdc',
            name='temperature',
            field=models.TextField(blank=True, null=True),
        ),
    ]
