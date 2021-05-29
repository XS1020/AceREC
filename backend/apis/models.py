from django.db import models

# Create your models here.


class Recom_Data(models.Model):
    updated_time = models.DateTimeField(auto_now=True)
    paper_id = models.BigIntegerField(db_index=True, unique=True)
    belong = models.IntegerField(db_index=True)
    embedding = models.CharField(default='', max_length=4096)

    class Meta:
        ordering = ['belong']


class Record(models.Model):
    updated_time = models.DateTimeField(auto_now=True)
    paper_id = models.BigIntegerField(db_index=True)
    user_id = models.BigIntegerField(db_index=True)

    class Meta:
        ordering = ['updated_time']


