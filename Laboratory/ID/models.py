from django.db import models

# Create your models here.
class Details(models.Model):
    aadhaar_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=100)
    caste = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=100)
