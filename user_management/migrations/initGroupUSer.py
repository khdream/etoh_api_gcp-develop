# create the first GROUPACCESS called "ADMIN" et first user with "ADMIN" group

from django.db import migrations
from django.contrib.auth.models import User
from user_management.models import GroupAccess, APIuser


def init_group_user(apps, schema_editor):
    group = GroupAccess.objects.all().filter(name="ADMIN").first()
    if group is None: #test there is no group called "ADMIN"
        group = GroupAccess.objects.create(name="ADMIN")
        group.save()

    user = User.objects.all().filter(username="user_admin").first()
    if user is None: #test there is no group called "ADMIN"
        user = User.objects.create_user("user_admin")
        apikey = "1234ABCDabcde"
        user.set_password(apikey)
        user.save()
    
    apiUser = APIuser.objects.all().filter(user=user).first()
    if apiUser is None: #test there is no group called "ADMIN"
        apiUser = APIuser.objects.create(user=user)
        apiUser.groupAccess.add(group)
        apiUser.save()



class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0006_alter_apistatistics_user'),
    ]

    operations = [
        migrations.RunPython(init_group_user),
    ]
