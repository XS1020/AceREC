from django.db import models

# Create your models here.




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
        ordering = ['-updated_time']


