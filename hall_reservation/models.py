from django.db import models

# Create your models here.


class Hall(models.Model):
    name = models.CharField(max_length=64)
    seats = models.IntegerField()
    projector = models.BooleanField()

