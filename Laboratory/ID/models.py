from django.db import models

# Create your models here.
class Details(models.Model):
    qrcode = models.ImageField(upload_to="images/")
    id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=100)
    caste = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=100)
