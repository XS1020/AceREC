from django.db import models

# Create your models here.


class Cite_Rec_Cache(models.Model):
    paper_id = models.BigIntegerField(db_index=True)
    field_id = models.IntegerField(db_index=True)
    Update_time = models.DateTimeField(auto_now=True)

    class Meta:
    	ordering = ['Update_time']
    	
