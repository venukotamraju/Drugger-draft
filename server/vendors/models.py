from django.db import models
from medicines.models import MedicineList

# Create your models here.

# for list of vendors
class VendorList(models.Model):
    vendor_id = models.BigAutoField(primary_key = True)
    vendor_name = models.CharField(max_length = 30, null = False, blank = False)

    def __str__(self):
        return self.vendor_name

# for details of the vendor
class VendorDetails(models.Model):
    vendor_id = models.OneToOneField(VendorList,on_delete = models.CASCADE,primary_key = True, null = False, blank = False)
    vendor_address = models.CharField(max_length = 100, null = False, blank = False)
    vendor_dln = models.CharField("vendor's drug license number", max_length = 100, null = False)
    vendor_contact = models.CharField("vendor's contact number", max_length = 14, null = False)
    vendor_email = models.CharField("vendor's email address", max_length = 30, null = False)
    vendor_coordinates = models.CharField("vendor's geo-location co-ordinates(latitude, longitude)", max_length = 100, null = False)

    def __str__(self):
        return f"The details of vendor: {self.vendor_address,self.vendor_dln,self.vendor_contact,self.vendor_email,self.vendor_coordinates}"

# for vendor login credentials
class VendorCredentials(models.Model):
    vendor_id = models.OneToOneField(VendorList,on_delete = models.CASCADE,primary_key = True,db_column="vendor_id")
    vendor_email = models.CharField("vendor's email address", max_length = 30, null = False)
    vendor_key = models.CharField("vendor's password", max_length = 30, null = False)

    def __str__(self):
        return f"instance for credentials of {self.vendor_email}"

# for medicines available at the vendor
class VendorMedsSupply(models.Model):
    vendor= models.OneToOneField(VendorList,on_delete=models.CASCADE,primary_key = True,db_column = "vendor_id")
    medicine = models.OneToOneField(MedicineList,on_delete=models.DO_NOTHING,db_column = "medicine_id")

