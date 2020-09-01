from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class Beach(models.Model):
    name = models.CharField(default = "", max_length = 200)
    surfline_url = models.CharField(default = "", max_length = 500)
    latitude = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 7)
    longitude = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 7)
    beach_dir = models.PositiveIntegerField(default = 0)
    wind_speed = models.PositiveIntegerField(default = 0)
    wind_dir = models.PositiveIntegerField(default = 0)
    swell1_height = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 7)
    swell2_height = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 7)
    swell1_period = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 7)
    swell2_period = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 7)
    swell1_dir = models.PositiveIntegerField(default = 0)
    swell2_dir = models.PositiveIntegerField(default = 0)
    tide_height = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 7)
    water_temp = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 7)
    driving_dist = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 2)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
