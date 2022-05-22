from django.db import models
from datetime import date, datetime  


# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    id_customer = models.TextField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.name


class Message(models.Model):
    id_customer = models.TextField(unique=True, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'Message {self.id_customer}'


