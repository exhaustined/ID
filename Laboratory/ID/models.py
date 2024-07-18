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

class SharedDetails(models.Model):
    shared_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    name_shared = models.BooleanField(default=False)
    phone_shared = models.BooleanField(default=False)
    age_shared = models.BooleanField(default=False)
    sex_shared = models.BooleanField(default=False)
    caste_shared = models.BooleanField(default=False)
    address_shared = models.BooleanField(default=False)
    marital_status_shared = models.BooleanField(default=False)

    def shared_data_string(self):
        shared_fields = []
        if self.name_shared:
            shared_fields.append('Name')
        if self.phone_shared:
            shared_fields.append('Phone')
        if self.age_shared:
            shared_fields.append('Age')
        if self.sex_shared:
            shared_fields.append('Sex')
        if self.caste_shared:
            shared_fields.append('Caste')
        if self.address_shared:
            shared_fields.append('Address')
        if self.marital_status_shared:
            shared_fields.append('Marital Status')

        return ", ".join(shared_fields)
