from django.contrib import admin
from .models import (Booth, BoothManager, Bike,Car, Vehicle)

# Register your models here.
admin.site.register([Booth, BoothManager, Bike,Car, Vehicle])
