from django.db import models

# Create your models here.


class Organization(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)

class Item(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    item_type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

class Pricing(models.Model):
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    zone = models.CharField(max_length=50)
    base_distance_in_km = models.DecimalField(max_digits=5, decimal_places=2)
    km_price = models.DecimalField(max_digits=5, decimal_places=2)
    fix_price = models.DecimalField(max_digits=10, decimal_places=2)