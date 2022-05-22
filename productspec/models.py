from django.db import models
from datetime import date, datetime  
from core.models import Country
from appellation.models import ViticultureZone

# Create your models here.

class Assemble(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table='productspec_blend'

    def __str__(self):
        return self.name

class AgingDefault(models.Model):
    id_productspec = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    type_aging = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Aging'
        verbose_name_plural = 'Agings'

    def __str__(self):
        return self.type_aging



class Robe(models.Model):
    color_name = models.CharField(max_length=255, null=True, blank=True)
    color_value = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


    class Meta:
        verbose_name = 'Robe'
        verbose_name_plural = 'Robes'
        db_table='productspec_color'

    def __str__(self):
        return self.name_colour




class WineProfileCDC(models.Model):
    color_id = models.ForeignKey(
        Robe, on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_profile_cdc')
    # aging = models.ForeignKey(
    #     AgingDefault, on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_profile_cdc')
    taste_acidity = models.IntegerField(blank=True, null=True)
    taste_alcohol = models.IntegerField(blank=True, null=True)
    taste_body = models.IntegerField(blank=True, null=True)
    taste_sweetness = models.IntegerField(blank=True, null=True)
    arom_complexity = models.IntegerField(blank=True, null=True)
    arom_intensity = models.IntegerField(blank=True, null=True)
    arom_length = models.IntegerField(blank=True, null=True)
    note_general = models.TextField(blank=True, null=True)
    color_desc = models.TextField(blank=True, null=True)
    note_fruity = models.TextField(blank=True, null=True)
    note_acidity = models.TextField(blank=True, null=True)
    note_body = models.TextField(blank=True, null=True)
    note_intensity = models.TextField(blank=True, null=True)
    temperature = models.TextField(blank=True, null=True)
    opening_time = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


    class Meta:
        verbose_name = 'WineProfileCDC'
        verbose_name_plural = 'WineProfileCDCs'
        db_table = 'productspec_profile'

    def __str__(self):
        return f'WineProfileCDC {self.id}'


class Vintage(models.Model):
    id_productspec = models.ForeignKey(
        'productspec.WineCDC', on_delete=models.SET_NULL, null=True, blank=True, related_name='vintages')
    apogee_min = models.DateTimeField(default=datetime.now, blank=True)
    apogee = models.DateTimeField(default=datetime.now, blank=True)
    apogee_max = models.DateTimeField(default=datetime.now, blank=True)
    quality = models.FloatField(blank=True, null=True)
    year = models.DateTimeField(default=datetime.now, blank=True)
    comment_vintage = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


    @property
    def vintage_integer(self):
        return self.year.year

    class Meta:
        verbose_name = 'Vintage'
        verbose_name_plural = 'Vintages'


class Aroma(models.Model):
    profile_wine_cdc = models.ForeignKey(
        WineProfileCDC, on_delete=models.CASCADE, blank=True, null=True, related_name='aromas')
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


    class Meta:
        verbose_name = 'Aroma'
        verbose_name_plural = 'Aromas'

    def __str__(self):
        return self.name


class CategoryLexicon(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


    class Meta:
        verbose_name = 'Lexicon Category'
        verbose_name_plural = 'Lexicon Categories'
        db_table = 'productspec_glossarycategory'

    def __str__(self):
        return self.name


class Lexicon(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        CategoryLexicon, on_delete=models.SET_NULL, null=True, blank=True, related_name='lexicons')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


    class Meta:
        verbose_name = 'Lexicon'
        verbose_name_plural = 'Lexicons'
        db_table = 'productspec_glossary'

    def __str__(self):
        return self.name

class LinkGlossaryCategory(models.Model):
    id_lexique = models.ForeignKey( Lexicon , on_delete=models.SET_NULL, null=True, blank=True, related_name='glossary_category')
    id_categorie = models.ForeignKey(
        CategoryLexicon, on_delete=models.SET_NULL, null=True, blank=True, related_name='glossary_category')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table='productspec_linkglossarycategory'



class GrapeProfile(models.Model):
    taste_acidity = models.IntegerField(blank=True, null=True)
    taste_alcohol = models.IntegerField(blank=True, null=True)
    taste_body = models.IntegerField(blank=True, null=True)
    arom_complexity = models.IntegerField(blank=True, null=True)
    arom_intensity = models.IntegerField(blank=True, null=True)
    arom_length = models.IntegerField(blank=True, null=True)
    note_general = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


class Grape(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    varietal_profile_id = models.ForeignKey(
        GrapeProfile, on_delete=models.SET_NULL, null=True, related_name='grapes')
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    color_varietal = models.CharField(max_length=255, null=True, blank=True)
    technical_name = models.TextField(null=True, blank=True)
    origin_country_id = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.SET_NULL)
    survey_hectares = models.TextField(null=True, blank=True)
    date_servey_hectares = models.DateTimeField(default=datetime.now, blank=True)
    comment_varietal = models.TextField(blank=True, null=True)
    aromas = models.TextField(null=True, blank=True)
    description_taste = models.TextField(null=True, blank=True)
    description_visual = models.TextField(null=True, blank=True)
    skins = models.TextField(null=True, blank=True)
    cultural_aptitudes = models.TextField(null=True, blank=True)
    phenology = models.TextField(null=True, blank=True)
    susceptibility_diseases = models.TextField(null=True, blank=True)
    guard_potential = models.TextField(null=True, blank=True)
    yields = models.TextField(null=True, blank=True)
    maturity = models.TextField(null=True, blank=True)
    berry_size = models.TextField(null=True, blank=True)
    type_variety = models.TextField(null=True, blank=True)
    species = models.TextField(null=True, blank=True)
    clones = models.TextField(null=True, blank=True)
    year_cross = models.TextField(null=True, blank=True)
    creator = models.TextField(null=True, blank=True)
    name_origin_alphabet_origin = models.TextField(blank=True, null=True)
    name_origin_alphabet_latin = models.TextField(blank=True, null=True)
    name_en = models.TextField(blank=True, null=True)
    language_origin = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Grape'
        verbose_name_plural = 'Grapes'
        db_table = 'productspec_varietal'

    def __str__(self):
        return self.name


class GrapeAssembly(models.Model):
    grape = models.ForeignKey(
        Grape, on_delete=models.CASCADE, blank=True, null=True, related_name='grape_assembles')
    assemble = models.ForeignKey(
        Assemble, on_delete=models.SET_NULL, null=True, blank=True, related_name='grape_assemble')
    percentage = models.IntegerField(blank=True, null=True)
    main_accessory = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table='productspec_varietal_blend'

    def __str__(self):
        return f'GrapeAssembly { self.grape }'




class SugarDose(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type_product = models.TextField(blank=True, null=True)
    sweetness_min = models.FloatField(null=True, blank=True)
    sweetness_max = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Dose'
        verbose_name_plural = 'Doses'
        db_table = 'productspec_dosagesweetness'

    def __str__(self):
        return self.name


class WineCDC(models.Model):
    name = models.TextField(null=True, blank=True)
    wine_profile_cdc_id = models.ForeignKey(
        WineProfileCDC, on_delete=models.CASCADE, null=True, blank=True, related_name="wine_cdc")
    sugar_dose_id = models.ForeignKey(
        SugarDose, on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_cdc')
    id_app = models.ForeignKey(
        'appellation.Appellation', on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_cdc')
    id_blend_default = models.ForeignKey(
        Assemble, on_delete=models.CASCADE, null=True, blank=True, related_name='wine_cdc')
    color = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    list_dvitivini = models.TextField(blank=True, null=True)
    comment_descritpion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Wine CDC'
        verbose_name_plural = 'Wine CDCs'
        db_table = 'productspec_productspec'

    def __str__(self):
        return self.name

    def grape(self):
        if self.assemble and self.assemble.grape_assemble.all():
            return [grape_assemble.grape.name for grape_assemble in self.assemble.grape_assemble.all().select_related('grape')]
        return []

    def appellations(self):
        if self.appellation:
            return self.appellation.name
        return ''

    def appellation_id(self):
        if self.appellation:
            return self.appellation.id
        return ''

    def zone_appellation_id(self):
        if self.appellation and self.appellation.zone_appelation:
            return self.appellation.zone_appelation.id

    def dgc(self):
        if self.appellation:
            return self.appellation.name_dgc
        return ''

    def sugar_doses(self):
        return self.sugar_dose.name

    def denomination_wines(self):
        denomination_wine = self.denomination_wine.all().first()
        if denomination_wine:
            return self.denomination_wine.all().first().name
        return ''


class DenominationWine(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    order = models.CharField(max_length=255, blank=True, null=True)
    wine_cdc = models.ForeignKey(
        WineCDC, on_delete=models.CASCADE, blank=True, null=True, related_name='denomination_wine')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Denomination Wine'
        verbose_name_plural = 'Denominations Wine'
        db_table = 'productspec_dvitivini'

    def __str__(self):
        return self.name

class WineCDCLexicon(models.Model):
    id_productspec = models.ForeignKey(
       WineCDC, on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_cdc_lexicons')
    id_glossary = models.ForeignKey(
        Lexicon, on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_cdc_lexicons')
    coeff = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


    class Meta:
        verbose_name = 'WineCDCLexicon'
        verbose_name_plural = 'WineCDCLexicons'
        db_table='productspec_link_wine_glossary'

    def __str__(self):
        return f'WineCDCLexicon {self.id}'


class AromaProfile(models.Model):
    id_profile_vin_spec = models.ForeignKey( WineCDC , on_delete=models.SET_NULL, null=True, blank=True, related_name='aroma_profile')
    id_aroma = models.ForeignKey(
        Aroma, on_delete=models.SET_NULL, null=True, blank=True, related_name='aroma_profile')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table='productspec_link_aroma_profile'

class WineCDCDvitivini(models.Model):
    id_productspec = models.ForeignKey( WineCDC , on_delete=models.SET_NULL, null=True, blank=True, related_name='winecdc_dvitivini')
    id_dvitivini = models.ForeignKey(
        DenominationWine, on_delete=models.SET_NULL, null=True, blank=True, related_name='winecdc_dvitivini')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table='productspec_link_wine_dvitivini'

class PlantationVarietal(models.Model):
    id_varietal = models.ForeignKey( Grape , on_delete=models.SET_NULL, null=True, blank=True, related_name='plantation_varietal')
    id_zviti = models.ForeignKey(
        ViticultureZone, on_delete=models.SET_NULL, null=True, blank=True, related_name='plantation_varietal')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table='productspec_plantation_varietal'

class GrapeMainAccessory(models.Model):
    wine_cdc_id = models.ForeignKey(WineCDC, on_delete=models.SET_NULL, null=True, blank=True, related_name='varietal_main_accessory')
    grape = models.ForeignKey(Grape, on_delete=models.CASCADE,
                              blank=True, null=True, related_name="grape_main_accessory")
    main_accessory = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table='productspec_varietal_main_accessory'

    def __str__(self):
        return f'GrapeMainAccessory { self.grape }'


class GrapeParent(models.Model):
    id_parent = models.ForeignKey(Grape, on_delete=models.SET_NULL, null=True, blank=True, related_name='varietal_parent_parent')
    id_child = models.ForeignKey(Grape, on_delete=models.SET_NULL, null=True, blank=True, related_name='varietal_parent_child')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    class Meta:
        db_table = 'productspec_varietalparent'

class GrapeSyn(models.Model):
    id_parent = models.ForeignKey(Grape, on_delete=models.SET_NULL, null=True, blank=True, related_name='varietal_syn')
    name = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    class Meta:
        db_table = 'productspec_varietal_syn'