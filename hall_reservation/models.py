from django.db import models

# Create your models here.
from django.db.models import DO_NOTHING


class Hall(models.Model):
    name = models.CharField(max_length=64)
    seats = models.IntegerField()
    projector = models.BooleanField()


class Reservation(models.Model):
    date = models.DateTimeField()
    hall_id = models.ForeignKey('Hall', on_delete=DO_NOTHING)
    comment = models.TextField()

    class Meta:
        unique_together = ('date', 'hall_id')
