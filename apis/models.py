from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import numpy as np
import googlemaps
from rest_api_server.settings import GOOGLE_API_KEY as g_key
from math import radians, cos, sin, asin, sqrt

# Create your models here.

class Beach(models.Model):
    name = models.CharField(default = "", max_length = 200)
    surfline_url = models.CharField(default = "", max_length = 500)
    latitude = models.DecimalField(default = 0.0, max_digits = 11, decimal_places = 7)
    longitude = models.DecimalField(default = 0.0, max_digits = 11, decimal_places = 7)
    beach_dir = models.PositiveIntegerField(default = 0)
    wind_speed = models.PositiveIntegerField(default = 0)
    wind_dir = models.PositiveIntegerField(default = 0)
    swell1_height = models.DecimalField(default = 0.0, max_digits = 10, decimal_places = 7)
    swell2_height = models.DecimalField(default = 0.0, max_digits = 10, decimal_places = 7)
    swell1_period = models.PositiveIntegerField(default = 0)
    swell2_period = models.PositiveIntegerField(default = 0)
    swell1_dir = models.PositiveIntegerField(default = 0)
    swell2_dir = models.PositiveIntegerField(default = 0)

    def calc_dist(self, lat, lng):
        lon1 = radians(lng)
        lon2 = radians(self.longitude)
        lat1 = radians(lat)
        lat2 = radians(self.latitude)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

        c = 2 * asin(sqrt(a))

        r = 3956

        # calculate the result
        return(c * r)

    def to_np_array(self, lat, lng):
        dist = self.calc_dist(lat, lng)
        return np.array([
            self.beach_dir,
            self.wind_speed, self.wind_dir,
            self.swell1_height, self.swell2_height,
            self.swell1_period, self.swell2_period,
            self.swell1_dir, self.swell2_dir,
            dist
            ])


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
