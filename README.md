# How to run this application
Before starting the app make sure that you have docker installed on your machine.  
Also, if you are running this application in production environment, make sure you have set a strong **SECRET_KEY**.  
  
The first two commands will build and run two containers (database and application itself):  
```
docker compose build
docker compose --env-file compose.env up
```  
Then you will need to make migrations. This proccess shouldn't be done automatically, so you need to type in the next line:
```
docker-compose run web python3 manage.py migrate
```  
After theese manipulations, you will have this application running on **WEB_PORT** port of your machine.