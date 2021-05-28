from django.db import models

# Create your models here.

class Author_INFO(models.Model):
    local_id = models.AutoField(primary_key=True)
    remote_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30, db_index=True)
    user_name = models.CharField(max_length=30, unique=True)
    research_list = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
