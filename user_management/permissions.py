from rest_framework import permissions
from user_management.models import GroupAccess, APIuser, APIstatistics

class accessGroupPermission(permissions.BasePermission):
    """
    Global permission check for API access
    """

    def has_permission(self, request, view):
        #permission related to group <-> method.path
        if self.checkAPIpermissions(request):
            #add statistics counter
            stats = APIstatistics.objects.create(user=request.user.apiuser, url=request.path)
            stats.save()
            return True

        return False

    #permission related to group <-> method.path
    #check if the user's group has permission for this method.path
    def checkAPIpermissions(self, request):
        api = request.method + "." + request.path
        for g in request.user.apiuser.groupAccess.all():
            if g.name == "ADMIN":
                return True #ADMIN group have all permissions
            group =  GroupAccess.objects.all().filter(name=g.name).first()
            listAPI = group.apiList.split(";")
            # if listAPI contains * at the end "/users/*", it means you have to compare the begining of the path
            for apiName in listAPI:
                if "*" in apiName:
                    if api.startswith(apiName[:len(apiName)-1]): #-1 to remove *
                        return True
            #normal test    
            if api in listAPI:
                return True
        return False
