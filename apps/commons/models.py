from django.db import models
from django.contrib.auth.models import User
from .utils import (validate_phone)
from django.core.validators import MinLengthValidator


# Create your models here.
#########################################################################
#               Notification for Each User

class Notification(models.Model):
    # each user will have many Notification with them
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(help_text="Enter notification message here.")



########################################################################
#           Detail for Each User
class SystemBaseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perm_address = models.CharField(max_length=50, help_text="Enter your permanent address")
    curr_address = models.CharField(max_length=50, help_text="Enter your current address",)
    mobile = models.CharField(max_length=10, validators=[validate_phone])

    class Meta:
        abstract = True

#######################################################################
#                   Admin for the System
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, validators=[validate_phone])
    image = models.ImageField(upload_to="admins")

    def __str__(self):
        return f"Admin : {self.user.username}"

##############################################################
#           Owner of vehicle both Rentable and Bookable
class Owner(SystemBaseUser):
    def __str__(self):
        return f"Owner : {self.user.username}"

#####################################################################
#            Customer Service Representative of the System
class CSR(SystemBaseUser):
    salary = models.PositiveIntegerField()

    def __str__(self):
        return f"CSR : {self.user.username}"


######################################################################
#                       Customer
class Customer(SystemBaseUser):
    dob = models.DateField()
    # license document provided
    license_doc = models.ImageField(upload_to='customer/licenses', null=True, blank=True)

    def __str__(self):
        return f"Customer : {self.user.username}"


########################################################################
#                   Distinguish Customer is Normal or Licensed Customer
class CustomerType(models.Model):
    licensed = models.BooleanField(default=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    # 1 or more customer is verified by 1 CSR
    verifier = models.ForeignKey(CSR, on_delete=models.SET_NULL, null=True,)





