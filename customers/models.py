from django.db import models
from django.utils import timezone
import random
import string
from datetime import datetime, timedelta

# Create your models here.

# for list of customers

class CustomerList(models.Model):
    customer_id = models.BigAutoField("id of the customer", primary_key = True)
    customer_name = models.CharField("name of the customer", max_length = 50 )

    def __str__(self):
        return self.customer_name

# for details of customers

class CustomerDetails(models.Model):
    customer_id = models.OneToOneField("CustomerList",on_delete = models.CASCADE, primary_key = True, db_column = "customer_id")
    customer_contact = models.CharField("mobile number of the customer", max_length = 13)
    customer_coordinates = models.CharField("location of the customer", max_length = 100)

# for the search history of the customer

class CustomerSearch(models.Model):
    customer_id = models.OneToOneField("CustomerList",on_delete = models.CASCADE, primary_key = True, db_column = "customer_id")
    customer_search = models.CharField("search word history of the customer", blank = True)

    def __str__(self):
        return f"search history of the customer is : {customer_search}"

# for otp of the customer
class CustomerOTP(models.Model):
    customer_id = models.OneToOneField(CustomerList,on_delete=models.CASCADE,primary_key=True,db_column="customer_id")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp = ''.join(random.choices(string.digits, k=6))
        self.created_at = datetime.now()
        self.save()

    def is_valid(self):
        # OTP is valid for 10 minutes
        return timezone.now()<self.created_at + timedelta(minutes=10) 
