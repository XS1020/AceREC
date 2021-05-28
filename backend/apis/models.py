from django.db import models

# Create your models here.

class Louvain_Res(models.Model):
	updated_time = models.DateTimeField(auto_now=True)
	paper_id = models.BigIntegerField(db_index=True, unique=True)
	belong = models.IntegerField(db_index=True)

	class Meta:
		ordering = ['belong']

