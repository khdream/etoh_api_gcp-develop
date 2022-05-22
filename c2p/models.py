from django.db import models
from client.models import Client
from datetime import date, datetime  

# Create your models here.


class Order(models.Model):
    id_client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    id_stocklist = models.ForeignKey(
        'bottle.StockList', on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    date = models.DateTimeField(default=datetime.now, blank=True)
    id_cmd_ext = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    id_customer_ext = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    quantity = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order { self.date }'

class PlateformAttribute(models.Model):
    id_platform  = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    name = models.TextField(blank=True, null=True)
    id_feature = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    id_parent = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

class PlateformCategory(models.Model):
    id_platform  = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    name = models.TextField(blank=True, null=True)
    id_category = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    id_parent = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

class PlateformStockNull(models.Model):
    id_platform  = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    done = models.BooleanField()
    id_plateform = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    id_stocklist = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

class ProductToUpdate(models.Model):
    id_platform = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    id_external = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    id_trigger_ext = models.BigIntegerField(blank=True, null=True) #Unknowed ID
    value = models.CharField(blank=True, null=True, max_length=10)
    date_to_do =models.DateField(null =True,blank=True)
    done = models.BooleanField()
    error = models.BooleanField()
    noimage = models.BooleanField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)