
from django.db import models
from client.models import Client
from datetime import date, datetime  
from appellation.models import AdminZone

# Create your models here.



class Alphabet(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

class Language(models.Model):
    id_alphabet = models.ForeignKey(Alphabet, on_delete=models.CASCADE,related_name='languages')
    name = models.CharField(max_length=255)
    name_fr = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    originalname_originalalphabet = models.CharField(max_length=255)
    originalname_latinalphabet = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

class Country(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    zone_admin = models.ForeignKey(
        AdminZone, on_delete=models.SET_NULL, null=True, blank=True, related_name='countries')
    id_language = models.ForeignKey(Language,on_delete=models.CASCADE, related_name='countries')
    originalname_originalalphabet = models.TextField(blank=True, null=True)
    originalname_latinalphabet = models.TextField(blank=True, null=True)
    
    name_fr = models.TextField(blank=True, null=True)
    name_en = models.TextField(blank=True, null=True)
    name_en_full = models.TextField(blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    code_isoalpha2 = models.CharField(max_length=2, blank=True, null=True)
    code_isoalpha3 = models.CharField(max_length=3, blank=True, null=True)
    code_isonum = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name