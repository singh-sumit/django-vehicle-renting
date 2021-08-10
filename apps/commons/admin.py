from django.contrib import admin
from .models import (Customer, CustomerType, Owner, CSR, Admin)

# Register your models here.

admin.site.register([Admin, Customer, CustomerType, Owner, CSR, ])
