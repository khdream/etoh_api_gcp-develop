# etoh_api_gcp

## Installation info

### install requirements
1. Create virtualenv for the project , activate it https://docs.python.org/3/library/venv.html
2. Clone project 
3. pip install -r requirements.txt 

### postgres setup
1. First have to install psql https://www.postgresql.org/docs/13/install-procedure.html
2. Second have to create user - remember the user and password , will use it later https://www.postgresql.org/docs/13/sql-createuser.html 
3. Third have to create database - remember database name , will use it later  https://www.postgresql.org/docs/13/sql-createdatabase.html


### connect database to the project
1. create .env file in main_api directory you can check the sample 
2. you have to put there your database credentials and your Algolia keys 
3. python manage.py migrate


## CRUD info 
1. For Every app in the project there is an urls.py file , there you can check the how to call every model in the API
2. You can alternatively check localhost:8000/swagger for swagger ui

## Services 
1. Autocomplete:
* For every endpoint you in autocomplete endpoints we are using algolia by default but if you want to make the search withou algolia you can add ?source=True as query_parameter
* autocomplete endpoints 
---
* amv/autocomplete-food/{ query }
* wse/vineyard/autocomplete/{ query }
* wse/region/autocomplete/{ query }
* wse/grape/autocomplete/{ query }
* wse/country/autocomplete/{ query }
* wse/autocomplete/{ field }/{ query }
* wse/get/wine?{ query_params }
* wse/get/wine_id?{ query_params }
* wse/corrector/{ field }/{ query }
* wse/geovinum/{ field }/{ query }
* wse/cleaner/{ query }
* wmk/autocomplete{ query }
* geo/autocomplete{ query }
* geo/corrector/{ query }
* 
---
## GCLOUD deploy
### ROLE (roles/appengine.deployer)

1. You have to authenticate in google https://cloud.google.com/sdk/gcloud/reference/auth
2. You have to config the project
* ```gcloud components update```
* ```gcloud config set project {gcloud_project_id}``` 
3. You have to run ```gcloud app deploy {{app_env.yaml}}``` Example for dev env: `gcloud app deploy app_dev.yaml`
4. If you have changes in your database , you have to connect with the gcp instance. 
Role 'roles/cloudsql.client' and 'roles/cloudsql.instanceUser' are required to connect to database.
* ```wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy```
* ```chmod +x cloud_sql_proxy```
* ```export GOOGLE_CLOUD_PROJECT=api-etoh-back-prod```
* ```export USE_CLOUD_SQL_AUTH_PROXY=true```
* ```./cloud_sql_proxy -instances="api-etoh-back-prod:europe-west1:bd-standard"=tcp:5432```
* Now you have instance running on your local machine , you have to change main_api/.env file. 
Credentials can be found on Google Secret Manager. 
--- 
* DATABASE_NAME={gcloud_name_of_database}
* DATABASE_HOST=127.0.0.1
* DATABASE_USER={gcloud_userof_database}
* DATABASE_PASSWORD={gcloud_password_of_database}
* DATABASE_PORT=5432 
---
* please before deploy revert back changes of this file 
* then you can run migration command , ```python manage.py makemigration``` , ```python manage.py migrate```
* you can also create super user for admin panel from here

## Auto deploy 
1. On push in main branch the changes will be deployed , but be careful there is no linters

## .env
1. You have to create .env file in main_api directory
2. You can store every type of secure data there


## Secret Manager
### ROLE (roles/secretmanager.secretVersionManager)
### If you want to change the secretmanager
1. gcloud secrets create django_settings --data-file main_api/.env
2. gcloud secrets describe django_settings
3. gcloud secrets versions access latest --secret django_settings
4. rm main_api/.env - to run project localy you will need .env
5. gcloud secrets add-iam-policy-binding django_settings --member serviceAccount:api-etoh-back-prod@appspot.gserviceaccount.com --role roles/secretmanager.secretAccessor
* You may have to delete the existing Secret Manager
### If you want to add a new version secretmanager
gcloud secrets versions add dev_django_settings --data-file=main_api/.env 
## Algolia
1. To rebuild index got to /algolia-reindex 
2. There is a cron on every 5 minutes that rebuild it. You can change it by changing the shcedule in cron.yaml
3. In every app there are index.py file there is fields and serach fields for every model that we want to index

## API links   
1. If you want to use API without gateway - https://api-etoh-back-prod.ew.r.appspot.com/
2. With gateway you will need API KEY - https://etoh-api-gateway-4kvtadw.ew.gateway.dev/amv?key=AIzaSyAGGsK_I8-FZi2g_dtTDkt8NFIqvn89I4k

## Create endpoint 
1. You have to create ViewSet in views.py  (https://www.django-rest-framework.org/api-guide/viewsets/)
2. You have to add it in the router
3. You have to generate new openapi-appengine.yaml - go to /swagger.json  and change the file with this content
* Tips
* Remove slashes after endpoints: ('/amv/') -> ('/amv')
* Find every endpoints that are with the same operationId - change it they have to be unique



## admin
1. For better visualization and control of your database you can go at https://api-etoh-back-prod.ew.r.appspot.com/admin/
2. To createsuper user for here you have to run the remote database locally and run the command 
* python manage.py createsuperuser  - and to pass the credentials 
3. initially I added user : admin | password : admin , but it will be good to be deleted

## JWT Token, Users management and Statistics
This application is in the folder : user_management.
* First to do is the section : "Users management - INSTALLATION" below
* Note: read section "Activation" below to activate or deactivate this application.
* To try it : read section "Tutorial" at the end

### Connection
To access to an url you have to be authentified and use your ACCESS TOKEN
1. for authentification use: GET /authentication/?apikey=your_apikey or POST /authentication/apikey/ (apikey in parameter) you will receive your ACCESS and REFRESH tokens
2. to do any request use the ACCESS TOKEN in the header : -H 'Authorization: Bearer access_token'

This token is valid for 1 hour, to refresh it use : /api/token/refresh/ with  -d '{"refresh":"refresh_token"}'

### JWT : Tokens lifetimes

Lifetimes are set in settings.py :
* SIMPLE_JWT = {
*     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
*     'REFRESH_TOKEN_LIFETIME': timedelta(minutes=60),


### Activation
To deactivate security and authorize any connections comments these 2 lines in settings.py :

*     'DEFAULT_PERMISSION_CLASSES': (
*         'rest_framework.permissions.IsAuthenticated',
*         'user_management.permissions.accessGroupPermission',

### Users management - permissions by groupAccess
groupAccess define which API can be called by this group.

* groupAccess have a name and apiList
  * example: "GROUP1" and "POST./users/;GET./wine/bottle;"
* apiList: list of pattern: method.url ending by ;
* pattern ending by * means all urls starting by this pattern : "GET./users/*" means all GET starting by /users/ like /users/test/
* allowed methods are: GET, POST, PUT, DELETE

* "ADMIN" group has all permissions.

* List all groups: GET /groupaccess/
* View a group: GET /groupaccess/name/
* Add a new group: POST /groupaccess/ with name in parameter
* Delete a  group: DELETE /groupaccess/name/
* Change group name: PUT /groupaccess/ with newName in parameter
* Add an authorized url: POST  /groupaccess/addAPI/name/ with api in parameter
* Remove an authorized url: POST  /groupaccess/deleteAPI/name/ with api in parameter

### Users management - Users
To be authentificated you need a user account.

* List all users: GET /users/
* View a user: GET /users/username/
* Add a new user: POST /users/ with parameters: username and apikey (optional if apikey is not provided a new one is generated)
* Delete a user: DELETE /users/username/
* Change user apikey: PUT /users/username/ with parameter: apikey (optional if apikey is not provided a new one is generated)
* Add a group : POST /users/addGroupAccess/username/ with parameter: groupAccessName
* Remove a group : POST /users/deleteGroupAccess/username/ with parameter: groupAccessName 

### Users management - INSTALLATION
Run as usual python manage.py migrate
The first accessGroup is created and is called "ADMIN" with give all access.
AND a first user called "user_admin" and apkey="1234ABCDabcde" is created with "ADMIN" Group.
So you have to change it for production.


### Statistics
Everytime a user calls an API it is recorded


Get counter of a user for an api: GET /stats/username 
*  with parameters:
*   api: name of url ie. "/users/"
*   after_dateTime: records done after this dateTime ie. "2022-02-09 10:00:00"
*   before_dateTime: records done before this dateTime ie. "2022-02-10 23:00:00"

## Tutorial JWT connection and User Management
1. Connection use your apikey
* ```curl -X POST http://127.0.0.1:8000/authentication/apikey/ -H "Content-Type: application/json" -d '{"apikey":"1234ABCD"}'```
* the response gives you the ACCESS token

2. Create your first group : "GROUP1"
* ```curl -X POST -H "Content-Type: application/json" -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' -d '{"name": "GROUP1"}' http://127.0.0.1:8000/groupaccess/```

3. Add 2 authorized APIs to the group : POST and GET users
* ```curl -X POST -H "Content-Type: application/json" -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' -d '{"api": "POST./users/*"}' http://127.0.0.1:8000/groupaccess/addAPI/GROUP1/```
* ```curl -X POST -H "Content-Type: application/json" -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' -d '{"api": "GET./users/*"}' http://127.0.0.1:8000/groupaccess/addAPI/GROUP1/```

4. Create a new user : "user1"
* ```curl -X POST -H "Content-Type: application/json" -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' -d '{"username": "user1","apikey":"123abc"}' http://127.0.0.1:8000/users/```

5. Add a group to "user1"
* ```curl -X POST -H "Content-Type: application/json" -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' -d '{"groupAccessName": "GROUP1"}' http://127.0.0.1:8000/users/addGroupAccess/user1/```

6. Statistics : how many times "user1" called "/users/" api between the two dates: 2022-02-09 10:00:00 and 2022-02-10 23:00:00
* ```curl -X GET -H "Content-Type: application/json" -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'  -d '{"api": "/users/", "before_dateTime":"2022-02-10 23:00:00", "after_dateTime":"2022-02-09 23:00:00"}' http://127.0.0.1:8000/stats/user1/```

## Environments
There are 3 environments for the application:
- dev : https://dev-dot-api-etoh-back-prod.ew.r.appspot.com
- preprod : https://preprod-dot-api-etoh-back-prod.ew.r.appspot.com
- prod : https://prod-dot-api-etoh-back-prod.ew.r.appspot.com

Each environment is deployed on a separate App Engine service
![App engine services](doc/app-engine-service.png "App engine services")

The 3 versions can be active at the same time.

Each App Engine service can have one or multiple active versions.

Each environment use a different secret manager key (https://console.cloud.google.com/security/secret-manager?project=api-etoh-back-prod&supportedpurview=project)
![Secret manager](doc/secret-manager.png "Secret manager")
[Link to view or update secret](https://console.cloud.google.com/security/secret-manager?project=api-etoh-back-prod&supportedpurview=project)

For example, if you want to modify the database settings for the preprod env, you must add a new version of the preprod secrets: (https://console.cloud.google.com/security/secret-manager/secret/preprod_django_settings/ versions?project=api-etoh-back-prod&supportedpurview=project)

Each environment is connected to a separated Postgres database:
- dev_api
- preprod_api
- prod_api

There are only one user for each database who can access and edit it, for example the 'user_dev' user cannot access the 'prod_api' database.
Database settings are stored in the secret manager.

We use Google Cloud Build to auto deploy version based on Github branch name, We have 3 cloud build triggers on each git push. 
`cloudbuild.yaml` is the config file: 
- auto-deploy-dev on branch `develop`
- auto-deploy-preprod on branch `preprod`
- auto-deploy-prod on branch `prod`
![Cloud Build](doc/cloud-build.png "Cloud Build")
![Github](doc/github.png "Github")


On Algolia indexes will have a prefix `dev_` for indexes linked to the dev environment and `preprod_` for those linked to the preprod environment and `prod_` for those linked to the prod environment.
We have api key per environment to isolate each env. For example for dev there is a key that can only access indexes that start with 'dev_*'.

The gcp permissions needed for all envs are:
- 'roles/appengine.serviceAdmin' (https://cloud.google.com/appengine/docs/standard/python/roles#predefined_roles)
- 'roles/cloudsql.client' and 'roles/cloudsql.instanceUser' (https://cloud.google.com/iam/docs/understanding-roles#cloud-sql-roles)