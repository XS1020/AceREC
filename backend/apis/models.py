from django.db import models

# Create your models here.


class Recom_Data(models.Model):
    updated_time = models.DateTimeField(auto_now=True)
    paper_id = models.BigIntegerField(db_index=True, unique=True)
    belong = models.IntegerField(db_index=True)

    class Meta:
        ordering = ['belong']

class Embedding(models.Model):
    paper_id = models.BigIntegerField(db_index=True)
    updated_time = models.DateTimeField(auto_now=True)
    Index = models.SmallIntegerField()
    Embnum = models.FloatField(default=0)

    class Meta:
        ordering = ['paper_id', 'Index']




class Record(models.Model):
    updated_time = models.DateTimeField(auto_now=True)
    paper_id = models.BigIntegerField(db_index=True)
    local_id = models.IntegerField(db_index=True)
    remote_id = models.BigIntegerField(db_index=True)

    rectypes = (
        (1, 'view'),
        (2, 'click')
    )
    rtype = models.IntegerField(choices=rectypes, default=1)

    class Meta:
        ordering = ['updated_time']


class Paper_Field(models.Model):
    paper_id = models.BigIntegerField(db_index=True)
    field_id = models.IntegerField(db_index=True)
