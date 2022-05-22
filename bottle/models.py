from django.db import models

from productspec.models import Assemble
from datetime import date, datetime  
from django.contrib.gis.db import models as gis_models
from client.models import Client
from productspec.models import AgingDefault, WineProfileCDC,Vintage



class WineMakerProfile(models.Model):
    taste_acidity = models.IntegerField(blank=True, null=True)
    taste_alcohol = models.IntegerField(blank=True, null=True)
    taste_body = models.IntegerField(blank=True, null=True)
    taste_sucrosite = models.IntegerField(blank=True, null=True)
    aroma_complexity = models.IntegerField(blank=True, null=True)
    aroma_intensity = models.IntegerField(blank=True, null=True)
    aroma_length = models.IntegerField(blank=True, null=True)
    general_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'WineMakerProfile'
        verbose_name_plural = 'WineMakerProfiles'

    def __str__(self):
        return f'WineMakerProfile {self.id}'


class WineMaker(models.Model):
    winemaker_profile = models.ForeignKey(
        WineMakerProfile, on_delete=models.SET_NULL, null=True, related_name='winemakers')
    country = models.ForeignKey(
        'core.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='winemaker')
    name = models.CharField(max_length=255, null=True,
                            blank=True, unique=True)
    siren = models.TextField(null=True, blank=True)
    viticulture = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(default=datetime.now, blank=True)
    address = models.TextField(null=True, blank=True)
    gps_location = gis_models.GeometryField(blank=True, null=True)
    type_winemaker = models.TextField(null=True, blank=True)
    comment_winemaker = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    google_place_id = models.TextField(null=True, blank=True)
    google_maps_url = models.TextField(null=True, blank=True)
    website = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    classement = models.TextField(null=True, blank=True)
    id_import = models.BigIntegerField(null=True, blank=True)
    lat = models.TextField(null=True, blank=True)
    lng = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'WineMaker'
        verbose_name_plural = 'WineMakers'
        db_table = 'bottle_producer'

    def __str__(self):
        return self.name


class WineBottle(models.Model):
    wine_profile_cdc = models.ForeignKey(
        WineProfileCDC, on_delete=models.CASCADE, blank=True, null=True, related_name='wine_bottle')
    vintage = models.ForeignKey(
        Vintage, on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_bottles')
    winemaker = models.ForeignKey(
        WineMaker, on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_container')
    assemble = models.ForeignKey(
        Assemble, on_delete=models.CASCADE, blank=True,  null=True, related_name='wine_bottle_assemble')
    comment_degustation = models.TextField(blank=True, null=True)
    comment_vinification = models.TextField(blank=True, null=True)
    comment_viticulture = models.TextField(blank=True, null=True)
    certification = models.TextField(blank=True, null=True)
    alcohol = models.FloatField(blank=True, null=True)
    name_tank = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Wine Bottle'
        verbose_name_plural = 'Wine Bottles'
        db_table='bottle_product'

    def __str__(self):
        return f'WineBottle {self.id}'


class Bottle(models.Model):
    wine_bottle = models.ForeignKey(
        WineBottle, on_delete=models.CASCADE, related_name='bottles', blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    gtin = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=25, blank=True, null=True)
    container = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Bottle'
        verbose_name_plural = 'Bottles'

    def __str__(self):
        return f'Bottle {self.id}'


class NoteGuide(models.Model):
    wine_bottle = models.ForeignKey(
        WineBottle, on_delete=models.CASCADE, blank=True, null=True, related_name='note_guides')
    guide = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Note Guide'
        verbose_name_plural = 'Note Guides'

    def __str__(self):
        return self.guide



class BottlePhoto(models.Model):
    bottle = models.ForeignKey(
        Bottle, on_delete=models.CASCADE, blank=True, null=True, related_name='bottle_photos')
    shooting = models.TextField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    source = models.TextField(blank=True, null=True)
    type_photo = models.TextField(blank=True, null=True)
    media_photo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Bottle Photo'
        verbose_name_plural = 'Bottle Photos'
        db_table = 'bottle_img'

    def __str__(self):
        return self.file_name

class Range(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True, related_name='range')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Range'
        verbose_name_plural = 'Ranges'

    def __str__(self):
        return self.name

class StockList(models.Model):
    id_range = models.ForeignKey(
        Range, on_delete=models.SET_NULL, blank=True, null=True, related_name='stocklists')
    id_bottle = models.ForeignKey(
        Bottle, on_delete=models.SET_NULL, blank=True, null=True, related_name='bottles')
    sku = models.TextField(null=True, blank=True)
    wine_name = models.CharField(max_length=25, null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    region = models.TextField(null=True, blank=True)
    subregion = models.TextField(null=True, blank=True)
    appellation = models.TextField(null=True, blank=True)
    label = models.TextField(null=True, blank=True)
    grape_assemble = models.TextField(null=True, blank=True)
    colour = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    vintage = models.TextField(null=True, blank=True)
    winemaker = models.TextField(null=True, blank=True)
    certification = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    weight = models.TextField(null=True, blank=True)
    alcohol = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    ranking = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    price_pre_taxe = models.FloatField(null=True, blank=True)
    vat = models.FloatField(null=True, blank=True)
    price_with_taxe = models.FloatField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    currency = models.CharField(max_length=5,  null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Stock list'
        verbose_name_plural = 'Stock lists'

    def __str__(self):
        return f'Stocklist {self.id}'


class Price(models.Model):
    stocklist = models.ForeignKey(
        StockList, on_delete=models.CASCADE, null=True, blank=True, related_name='bottle_prices')
    price = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=5,  null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    promo_price = models.FloatField(null=True, blank=True)
    start_promotion_date = models.DateTimeField(default=datetime.now, blank=True)
    end_promotion_date = models.DateTimeField(default=datetime.now, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Bottle price'
        verbose_name_plural = 'Bottles prices'

    def __str__(self):
        return f'BottlePrice {self.id}'
class Warehouse(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouses')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    # foreign key to warehouse_ext

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'

    def __str__(self):
        return self.name


class Stock(models.Model):
    stocklist = models.ForeignKey(
        StockList, on_delete=models.CASCADE, null=True, blank=True, related_name='stocks')
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='stocks')
    # foreign key to stock_ext TODO
    id_stock_ext = models.BigIntegerField(blank=True, null=True) # Unknowed ID
    quantity = models.IntegerField(null=True, blank=True)
    quantity_available = models.IntegerField(null=True, blank=True)
    quantity_ordered = models.IntegerField(null=True, blank=True)
    quantity_reserved = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return f'Stock {self.id}'
