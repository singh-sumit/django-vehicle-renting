from django.urls import path
from .views import (HomeView, CustomerRegisterView, OwnerRegisterView, OwnerLoginView, SystemAdminLoginView,
                    SystemAdminHomeView, UserLogoutView, AddCSRView)

app_name = 'commons'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('customer-signup/', CustomerRegisterView.as_view(), name="customer_signup"),
    path('owner-signup/', OwnerRegisterView.as_view(), name='owner_signup'),
    path('owner-signin/', OwnerLoginView.as_view(), name='owner_signin'),

    ############################################################################
    #                   System Admin Part
    path('sys/', SystemAdminLoginView.as_view(), name="admin-signin"),
    path('sys/home/', SystemAdminHomeView.as_view(), name="admin-home"),
    path('sys/add-csr/', AddCSRView.as_view(), name="admin-add-csr")

]
