from django.contrib import admin
from .models import (Booth, BoothManager, Bike, Car, Vehicle, BalanceSheet, InstantIncome)

# Register your models here.
admin.site.register([Booth, BoothManager, Bike,Car, Vehicle, InstantIncome, BalanceSheet])
