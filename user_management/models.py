from django.db import models
from django.contrib.auth.models import User


# GROUPACCESS model
class GroupAccess(models.Model):
    name = models.CharField(max_length=255, blank=False, default=None, unique=True)
    apiList = models.TextField(default="") #list of authorized api : format is method.url separated by ; , example: GET./users/;POST./users/create/;

    def __str__(self):
        return self.name

# USERS OF THE API model
class APIuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groupAccess = models.ManyToManyField(GroupAccess, default=None) #APIuser can have several groups to access to some apis

    def __str__(self):
        return self.user.username


# USERS OF THE API model
class APIstatistics(models.Model):
    user = models.ForeignKey(APIuser, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=False, default=None)
    createdDateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
