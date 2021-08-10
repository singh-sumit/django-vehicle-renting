from django.urls import path
from .views import (HomeView, CustomerRegisterView, OwnerRegisterView)

app_name = 'commons'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('customer-signup/', CustomerRegisterView.as_view(), name="customer_signup"),
    path('owner-signup/', OwnerRegisterView.as_view(), name='owner_signup'),

]
