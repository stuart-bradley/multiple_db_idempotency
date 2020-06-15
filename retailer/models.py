from django.db import models


class Retailer(models.Model):
    name = models.CharField(max_length=256)


class Outlet(models.Model):
    retailer_id = models.IntegerField()
    name = models.CharField(max_length=256)
