from django.db import models

# To migrate Models
# > python manage.py makemigrations User
# > python manage.py migrate User

# Create your models here.

class User_Info(models.Model):
    local_id = models.IntegerField(primary_key=True)
    remote_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=30, db_index=True)
    user_name = models.CharField(max_length=30, unique=True)
    affiliation = models.CharField(max_length=50)
    research_list = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    paper_num = models.IntegerField()

class User_Edu(models.Model):
    local_id = models.IntegerField(db_index=True)
    remote_id = models.BigIntegerField(db_index=True)
    year = models.IntegerField()
    action = models.CharField(max_length=20)
    institute = models.CharField(max_length=50)
    department = models.CharField(max_length=80)

class User_Work(models.Model):
    local_id = models.IntegerField(db_index=True)
    remote_id = models.BigIntegerField(db_index=True)
    year = models.IntegerField()
    action = models.CharField(max_length=20)
    institute = models.CharField(max_length=50)
    department = models.CharField(max_length=80)

class User_Interest(models.Model):
    local_id = models.IntegerField(db_index=True)
    remote_id = models.BigIntegerField(db_index=True)
    interest_field = models.IntegerField()

class User_Token(models.Model):
    local_id = models.IntegerField(primary_key=True)
    token = models.CharField(max_length=100)

class User_Papers(models.Model):
    local_id = models.IntegerField(db_index=True)
    remote_id = models.BigIntegerField(db_index=True)
    paper_id = models.BigIntegerField(db_index=True)
