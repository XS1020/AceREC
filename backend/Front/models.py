from django.db import models

# Create your models here.


class Cite_Rec_Cache(models.Model):
    paper_id = models.BigIntegerField(db_index=True)
    field_id = models.IntegerField(db_index=True)
    Update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['Update_time']


class Paper_Field(models.Model):
    paper_id = models.BigIntegerField(db_index=True)
    field_id = models.IntegerField(db_index=True)
    year = models.IntegerField(default=2008)


class Recom_Data(models.Model):
    updated_time = models.DateTimeField(auto_now=True)
    paper_id = models.BigIntegerField(db_index=True, unique=True)
    belong = models.IntegerField(db_index=True)

    class Meta:
        ordering = ['belong']


class Embeddings(models.Model):
    paper_id = models.BigIntegerField(db_index=True)
    updated_time = models.DateTimeField(auto_now=True)
    Embedding = models.CharField(max_length=2600)

    class Meta:
        ordering = ['paper_id']
