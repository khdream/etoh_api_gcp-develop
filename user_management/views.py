
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from user_management.serializers import UserSerializer, GroupAccessSerializer, APIstatisticsSerializer
from django.contrib.auth.models import User
from user_management.models import GroupAccess, APIuser, APIstatistics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status





#USERS MANAGEMENT
#
#
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


    #View a user: GET /username/
    #@out: username, group
    def retrieve(self, request, pk):
        username = pk
        user =  self.queryset.filter(username=username).first()
        if not user:
            return Response({'message': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not hasattr(user, 'apiuser'):
            return Response({'message': "apiuser does not exist for this user"}, status=status.HTTP_400_BAD_REQUEST)

        #for display
        listGroupNames=[]
        for g in user.apiuser.groupAccess.all():
            listGroupNames.append(g.name);

        serializer = self.get_serializer(user)
        return Response({"id": serializer.data["id"], "username":serializer.data["username"], "group":listGroupNames })



    #CREATE user: 
    #@in param: username, apikey if not defined autogenerated
    #@out: apikey, username of created user
    def create(self, request):
        username = request.data.get("username")
        apikey = request.data.get("apikey")
        if not username or len(username) == 0:
            return Response({'message': "Please define at least username"}, status=status.HTTP_400_BAD_REQUEST)

        if not apikey or len(apikey) == 0:
            apikey = User.objects.make_random_password(length=30)

        if self.checkAPIKEYexist(apikey):
            return Response({'message': "apikey already exists, please define a new one"}, status=status.HTTP_400_BAD_REQUEST)

        request.data["password"] = apikey

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            newUser = serializer.save()
            newUser.set_password(apikey)
            newUser.save()
            newAPIuser = APIuser(user=newUser)
            newAPIuser.save()
            return Response({"message": "created", "apikey":apikey, "username":serializer.data["username"]})
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    #UPDATE user for new apikey
    #@in param: new apikey if not defined autogenerated
    #@out: apikey, username of updated user
    def update(self, request, pk):
        username = pk
        apikey = request.data.get("apikey")
        if not apikey or len(apikey) == 0:
            apikey = User.objects.make_random_password(length=30)
        if self.checkAPIKEYexist(apikey):
            return Response({'message': "apikey already exists, please define a new one"}, status=status.HTTP_400_BAD_REQUEST)

        request.data["password"] = apikey

        user =  self.queryset.filter(username=username).first()
        if not user:
            return Response({'message': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(apikey)
        user.save()
        return Response({"message": "updated", "apikey":apikey, "username":username})



    #DELETE user:
    #@in: param: username, apikey
    #@out: username of deleted user
    def destroy(self, request, pk):
        username = pk
        user =  self.queryset.filter(username=username).first()
        if not user:
            return Response({'message': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({"message": "deleted","username":username})


    #ADD groupAccess for user:
    #@in param: group name
    #@out: username, groups
    @action(methods=['POST'], detail=False, url_path='addGroupAccess/(?P<username>[^/.]+)')
    def add_apiToList(self, request, username):
        groupAccessName = request.data.get("groupAccessName")
        group =  GroupAccess.objects.all().filter(name=groupAccessName).first()
        user =  self.queryset.filter(username=username).first()
        if not user:
            return Response({'message': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not groupAccessName or len(groupAccessName) == 0:
            return Response({'message': "Please define at least groupAccessName"}, status=status.HTTP_400_BAD_REQUEST)
        if not group:
            return Response({'message': "Group "+groupAccessName+" does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not hasattr(user, 'apiuser'):
            return Response({'message': "apiuser does not exist for this user"}, status=status.HTTP_400_BAD_REQUEST)

        user.apiuser.groupAccess.add(group) #add the group to the user
        
        #for display
        listGroupNames=[]
        for g in user.apiuser.groupAccess.all():
            listGroupNames.append(g.name);

        return Response({"message": "Group added", "username":user.username, "group":listGroupNames})


    #REMOVE groupAccess for user:
    #@in param: group name
    #@out: username, groups
    @action(methods=['POST'], detail=False, url_path='deleteGroupAccess/(?P<username>[^/.]+)')
    def delete_apiToList(self, request, username):
        groupAccessName = request.data.get("groupAccessName")
        group =  GroupAccess.objects.all().filter(name=groupAccessName).first()
        user =  self.queryset.filter(username=username).first()
        if not user:
            return Response({'message': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not groupAccessName or len(groupAccessName) == 0:
            return Response({'message': "Please define at least groupAccessName"}, status=status.HTTP_400_BAD_REQUEST)
        if not group:
            return Response({'message': "Group "+groupAccessName+" does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not hasattr(user, 'apiuser'):
            return Response({'message': "apiuser does not exist for this user"}, status=status.HTTP_400_BAD_REQUEST)

        user.apiuser.groupAccess.remove(group) #add the group to the user
        
        #for display
        listGroupNames=[]
        for g in user.apiuser.groupAccess.all():
            listGroupNames.append(g.name);

        return Response({"message": "Group removed", "username":user.username, "group":listGroupNames})

    # Returns True if a password already exists
    def checkAPIKEYexist(self,apikey):
        for user in User.objects.all():
            if check_password(apikey, user.password):
                return True
        return False



#GROUPS MANAGEMENT
#
#
class GroupAccessViewSet(ModelViewSet):
    serializer_class = GroupAccessSerializer
    queryset = GroupAccess.objects.all()

    #View a group: GET /name/
    #@out: name, apiList
    def retrieve(self, request, pk):
        name = pk
        group =  self.queryset.filter(name=name).first()
        if not group:
            return Response({'message': "Group "+name+" does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(group)
        return Response({"name":serializer.data["name"], "apiList":serializer.data["apiList"]})


    #CREATE GroupAccess: 
    #@in param: name, apiList
    #@out: name, apiList of created GroupAccess
    def create(self, request):
        name = request.data.get("name")
        listAPI = request.data.get("listAPI")
        if not name or len(name) == 0:
            return Response({'message': "Please define at least name"}, status=status.HTTP_400_BAD_REQUEST)

        group =  self.queryset.filter(name=name).first() #name should be unique
        if group:
            return Response({'message': "Group "+name+"  already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "created", "name":serializer.data["name"], "apiList":serializer.data["apiList"]})
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    #UPDATE GroupAccess: 
    #@in param: newName
    #@out: name, newname, apiList of updated GroupAccess
    def update(self, request, pk):
        name = pk
        newName = request.data.get("newName")
        if not newName or len(newName) == 0:
            return Response({'message': "Please define at least newName"}, status=status.HTTP_400_BAD_REQUEST)

        group =  self.queryset.filter(name=name).first()
        if not group:
            return Response({'message': "Group "+name+" does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(group,data={"name":newName})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated", "oldName":name, "name":serializer.data["name"], "apiList":serializer.data["apiList"]})
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    #DELETE GroupAccess:
    #@in param: name
    #@out: name of deleted GroupAccess
    def destroy(self, request, pk):
        name = pk
        group =  self.queryset.filter(name=name).first()
        if not group:
            return Response({'message': "Group "+name+" does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        group.delete()
        return Response({"message": "deleted","name":name})

    #ADD an authorized API to the group:
    #@in param: api, example: "POST./users/xxx/"
    #@out: name, apiList
    @action(methods=['POST'], detail=False, url_path='addAPI/(?P<name>[^/.]+)')
    def add_apiToList(self, request, name):
        api = request.data.get("api")
        group =  self.queryset.filter(name=name).first()
        if not api or len(api) == 0:
            return Response({'message': "Please define at least api"}, status=status.HTTP_400_BAD_REQUEST)
        if not group:
            return Response({'message': "Group "+name+" does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not self.checkAPIformat(api):
            return Response({'message': "Wrong API format"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(group)

        if api+";" in serializer.data["apiList"]:
            return Response({'message': "API already exists"}, status=status.HTTP_400_BAD_REQUEST)

        newapiList = serializer.data["apiList"]+api+";";
        serializer = self.get_serializer(group,data={"apiList":newapiList})
        if serializer.is_valid():
            serializer.save()        
            return Response({"message": "added", "name":serializer.data["name"], "apiList":serializer.data["apiList"]})
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    #REMOVE an authorized API to the group:
    #@in param: api, example: "POST./users/xxx/"
    #@out: name, apiList
    @action(methods=['POST'], detail=False, url_path='deleteAPI/(?P<name>[^/.]+)')
    def remove_apiToList(self, request, name):
        api = request.data.get("api")
        group =  self.queryset.filter(name=name).first()
        if not api or len(api) == 0:
            return Response({'message': "Please define at least api"}, status=status.HTTP_400_BAD_REQUEST)
        if not group:
            return Response({'message': "Group "+name+" does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(group)
        newapiList = self.removeAPIfromList(serializer.data["apiList"],api)
        serializer = self.get_serializer(group,data={"apiList":newapiList})
        if serializer.is_valid():
            serializer.save()        
            return Response({"message": "Remove", "name":serializer.data["name"], "apiList":serializer.data["apiList"]})
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    #api format is method.url : POST./users/path
    def checkAPIformat(self, api):
        methods=["POST","GET","PUT","DELETE"];
        if not "." in api or " " in api:
            return False

        apiSplit = api.split(".")
        method = apiSplit[0]
        if not method in methods:
            return False
        return True


    #api format is method.url : POST./users/path
    def removeAPIfromList(self, apiList, api):
        listAPI = apiList.split(";")
        if not api in listAPI:
            return apiList
        listAPI.remove(api)
        return ';'.join(listAPI)






#STATISTICS API
#
#
class StatisticsAPIViewSet(ModelViewSet):
    serializer_class = APIstatisticsSerializer
    queryset = APIstatistics.objects.all()

    #View a user statistics: GET /username/
    #@in: api : url path , after_dateTime: records done after this dateTime, before_dateTime: records done before this dateTime
    def retrieve(self, request, pk):
        username = pk
        api = request.GET["api"]
        after_dateTime = request.data.get("after_dateTime")
        before_dateTime = request.data.get("before_dateTime")
        userapi =  APIuser.objects.all().filter(user__username=username).first()
        if not userapi:
            return Response({'message': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        userStats =  self.queryset.filter(user=userapi)
        
        if api:
            userStats =  userStats.filter(url__startswith=api)
        if after_dateTime:
            userStats =  userStats.filter(createdDateTime__gt=after_dateTime)
        if before_dateTime:
            userStats =  userStats.filter(createdDateTime__lte=before_dateTime)

        return Response({"username":userapi.user.username, "count": userStats.count(), "api": api})







#AUTHENTIFICATION API
#
#
class AuthAPIView(APIView):
    permission_classes = (AllowAny,) #url public access to connect
    def get(self, request, format=None):  
        apikey=request.GET['apikey']
        for user in User.objects.all():
            if check_password(apikey, user.password):
                refresh = RefreshToken.for_user(user)
                JwtToken= {'refresh': str(refresh),'access': str(refresh.access_token),}
                return Response(JwtToken)
                
        return Response({'Authentification Failed'}, status=status.HTTP_401_UNAUTHORIZED)

    #POST Authentification
    def post(self, request, format=None):
        apikey=request.data.get('apikey')
        for user in User.objects.all():
            if check_password(apikey, user.password):
                refresh = RefreshToken.for_user(user)
                JwtToken= {'refresh': str(refresh),'access': str(refresh.access_token),}
                return Response(JwtToken)
                
        return Response({'Authentification Failed'}, status=status.HTTP_401_UNAUTHORIZED)
