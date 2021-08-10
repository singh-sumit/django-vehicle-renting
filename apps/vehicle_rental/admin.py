from django.contrib import admin
from .models import (Booth, BoothManager, Bike,Car)

# Register your models here.
admin.site.register([Booth, BoothManager, Bike,Car])
