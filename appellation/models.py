from django.db import models
from datetime import date, datetime  
from django.contrib.gis.db import models as gis_models

# Create your models here.


class AppellationZone(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)
    geom = gis_models.GeometryField(blank=True, null=True)
    ground = models.TextField(blank=True, null=True)
    subsoil = models.TextField(blank=True, null=True)
    climat = models.TextField(blank=True, null=True)
    elevetion_min = models.FloatField(null=True, blank=True)
    elevetion_max = models.FloatField(null=True, blank=True)
    elevetion_average = models.FloatField(null=True, blank=True)
    precipitation_min = models.FloatField(null=True, blank=True)
    precipitation_max = models.FloatField(null=True, blank=True)
    precipitation_average = models.FloatField(null=True, blank=True)
    situation = models.TextField(blank=True, null=True)
    sunshine = models.TextField(blank=True, null=True)
    temperature_min = models.FloatField(null=True, blank=True)
    temperature_max = models.FloatField(null=True, blank=True)
    temperature_average = models.FloatField(null=True, blank=True)
    orientation = models.TextField(blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    geology = models.TextField(blank=True, null=True)
    pedology = models.TextField(blank=True, null=True)
    lithology = models.TextField(blank=True, null=True)
    hierarchy = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Appelation Zone'
        verbose_name_plural = 'Appelation Zones'

    def __str__(self):
        return self.name


class AppellationPhoto(models.Model):
    appellation_zone = models.ForeignKey(
        AppellationZone, on_delete=models.CASCADE, blank=True, null=True, related_name='appellation_zone_photos')
    shooting = models.TextField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    source = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    media_photo = models.TextField(blank=True, null=True)
    gps_coordinates = gis_models.GeometryField(blank=True, null=True)

    class Meta:
        verbose_name = 'Appellation Photo'
        verbose_name_plural = 'Appellation Photos'
        db_table = f"appellation_image"

    def __str__(self):
        return self.file_name


class Appellation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    zone_appelation = models.ForeignKey(
        AppellationZone, on_delete=models.SET_NULL, null=True, blank=True, related_name='appellation')
    name_dgc = models.CharField(max_length=255, blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    etymology = models.TextField(blank=True, null=True)
    hierarchy = models.TextField(blank=True, null=True)
    volume_production = models.IntegerField(null=True, blank=True)
    dosage = models.ManyToManyField(
        'productspec.SugarDose', blank=True, related_name='appellations')
    # denomination_wine = models.ForeignKey(
    #     'wine.DenominationWine', on_delete=models.SET_NULL, blank=True, null=True, related_name='appellations')
    name_origin_alphabet_origin = models.TextField(blank=True, null=True)
    name_origin_alphabet_latin = models.TextField(blank=True, null=True)
    name_english_alphabet_latin = models.TextField(blank=True, null=True)
    language_origin = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    app_syn = models.ManyToManyField('Appellation', through='AppellationSyn', blank=True)

    class Meta:
        verbose_name = 'Appellation'
        verbose_name_plural = 'Appellation'

    def __str__(self):
        return self.name

class AppellationSyn(models.Model):
    id_app_ref = models.ForeignKey('Appellation',on_delete=models.CASCADE, related_name='Appellation_ref')
    id_app_syn = models.ForeignKey('Appellation',on_delete=models.CASCADE, related_name='Appellation_syn')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)




class Color(models.Model):
    appellation = models.ForeignKey(
        Appellation, on_delete=models.CASCADE, null=True, blank=True, related_name='appellation_colour')
    type_authorization = models.TextField(blank=True, null=True)
    color_authorization = models.TextField(blank=True, null=True)
    percentage = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Appellation Colour'
        verbose_name_plural = 'Appellation Colours'

    def __str__(self):
        return f'Color {self.id}'


class AppellationType(models.Model):
    id_app = models.ForeignKey(
        Appellation, on_delete=models.CASCADE, null=True, blank=True, related_name='appellation_type')
    type_authorization = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Appellation Type'
        verbose_name_plural = 'Appellation Types'

    def __str__(self):
        return f'AppellationType {self.id}'


class AdminZone(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)
    # zone_appelation = models.ForeignKey(
    #     AppellationZone, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_zones')
    hierarchy = models.TextField(blank=True, null=True)
    geom = gis_models.GeometryField(blank=True, null=True)
    link_za_zadm = models.ManyToManyField('AppellationZone', through='LinkZappZadmin', blank=True)

    class Meta:
        verbose_name = 'Zone Admin'
        verbose_name_plural = 'Zone Admins'

    def __str__(self):
        return self.name

    def code_insee(self):
        if self.plot_zone.all().first():
            return self.plot_zone.all().first().code_insee

    def as_dict(self):
         return {
             "objectID": self.id,
             "name": self.name,
             "parent": self.parent,
             "hierarchy": self.hierarchy,
         }


class LinkZappZadmin (models.Model):
    id_za = models.ForeignKey('AppellationZone',on_delete=models.CASCADE)
    id_zadm= models.ForeignKey('AdminZone',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

class LinkAppDvitivini (models.Model):
    id_app = models.ForeignKey('Appellation',on_delete=models.CASCADE)
    id_dvitivini_authorized= models.ForeignKey('productspec.DenominationWine',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


class PlotZone(models.Model):
    zone_admin = models.ForeignKey(
        AdminZone, on_delete=models.SET_NULL, blank=True, null=True, related_name='plot_zone')
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)
    zone_appelation = models.ForeignKey(
        AppellationZone, on_delete=models.SET_NULL, null=True, blank=True, related_name='plot_zones')
    hierarchy = models.TextField(blank=True, null=True)
    code_insee = models.CharField(max_length=25, null=True, blank=True)
    prefix = models.CharField(max_length=25, null=True, blank=True)
    section = models.CharField(max_length=25, null=True, blank=True)
    number = models.CharField(max_length=25, null=True, blank=True)
    geom = gis_models.GeometryField(blank=True, null=True)
    

    class Meta:
        verbose_name = 'Plot Zone'
        verbose_name_plural = 'Plot Zones'

    def __str__(self):
        return f'PlotZone {self.id}'


class ViticultureZone(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)
    zone_admin = models.ForeignKey(
        AdminZone, on_delete=models.SET_NULL, blank=True, null=True, related_name='viticulture_zone')
    hierarchy = models.TextField(blank=True, null=True)
    geom = gis_models.GeometryField(blank=True, null=True)
    name_origin_alphabet_origin = models.TextField(blank=True, null=True)
    name_origin_alphabet_latin = models.TextField(blank=True, null=True)
    name_english_alphabet_latin = models.TextField(blank=True, null=True)
    language_origin = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Viticulture zone'
        verbose_name_plural = 'Viticulture zones'

    def __str__(self):
        return self.name



