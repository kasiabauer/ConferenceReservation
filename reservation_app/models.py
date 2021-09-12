from django.db import models

# Create your models here.


class ConfRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()
    projector_availability = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class RoomReservation(models.Model):
    conf_room = models.ForeignKey(ConfRoom, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.CharField(max_length=1000, null=True)

    class Meta:
        unique_together = ('conf_room', 'date')
