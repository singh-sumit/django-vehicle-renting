from django.contrib import admin
from .models import (Customer,CustomerType, Owner, CSR)
# Register your models here.

admin.site.register([Customer,CustomerType, Owner, CSR])
