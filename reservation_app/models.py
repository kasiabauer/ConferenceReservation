from django.db import models

# Create your models here.


class ConfRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()
    projector = models.BooleanField()

