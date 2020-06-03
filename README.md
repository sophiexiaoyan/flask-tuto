first step: create database in mysql
```
mysql -u root -p
create database flaskr
```

second step: create tables in database
```
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
```

third step: run the application
```
python manager.py runserver
```
