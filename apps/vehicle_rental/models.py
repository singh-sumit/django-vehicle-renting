from django.db import models
from django.contrib.auth.models import User
from apps.commons.models import (Owner, SystemBaseUser)
from apps.commons.utils import (validate_phone, )
from django.core.validators import (MinLengthValidator)


# Create your models here.
#######################################################################################
#               Booth Manager
class BoothManager(SystemBaseUser):
    pass


############################################################################
#               Booth (a collection of vehicles to be rented)
class Booth(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=50)
    # 1 booth has 1 manager
    manager = models.OneToOneField(BoothManager, on_delete=models.SET_DEFAULT, default=0)


###############################################################
#               Vehicle Status
VEHICLE_STATUS = (
    ('AVAILABLE', 'AVAILABLE'),
    ('RESERVED', 'RESERVED')
)


#################################################################
#                   Vehicle to be rented

class Vehicle(models.Model):
    # B DE 1234
    plate_num = models.CharField(max_length=7, unique=True,
                                 help_text='Plate number like : BDE1234')
    brand = models.CharField(max_length=20)
    seats = models.PositiveIntegerField(help_text='Enter available seats')
    wheels_num = models.PositiveIntegerField(help_text='Enter wheels number of a vehicle')
    manufacturing_year = models.PositiveIntegerField(validators=[MinLengthValidator(4)])
    mileage = models.PositiveIntegerField()
    fare = models.PositiveIntegerField(help_text='Enter a fare for per day')
    status = models.CharField(max_length=50, choices=VEHICLE_STATUS,
                              default=VEHICLE_STATUS[0][1])
    # Many vehicle is owned by 1 Owner
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    # 1 vehicle is issued by 1 BoothManager
    issued_by = models.OneToOneField(BoothManager, on_delete=models.SET(BoothManager))
    # 1 vehicle may reside on Multiple Booth
    residing_booth = models.ForeignKey(Booth, on_delete=models.PROTECT)

    class Meta:
        abstract = True


#####################################################################
#                   Bike is sub class of Vehicle
class Bike(Vehicle):
    vehicle_type = models.CharField(max_length=10, default="Bike")

    def __str__(self):
        return f"Bike :{self.plate_num}"


#####################################################################
#                   Car is sub class of Vehicle
class Car(Vehicle):
    vehicle_type = models.CharField(max_length=10, default="Car")

    def __str__(self):
        return f"Car :{self.plate_num}"
