from django.db import models
from django.conf import settings

# Create your models here.
class Config_Perfil(models.Model):
    client = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_pomodoro = models.PositiveIntegerField(default=25)
    time_short_break = models.PositiveIntegerField(default=5)
    time_long_break = models.PositiveIntegerField(default=15)
    quantity_long_break = models.PositiveIntegerField(default=4)
    teste = models.CharField(max_length=20)
    type_sound = models.CharField(max_length=200, default="digital")
    def __str__(self):
        return self.client.username + "_client"