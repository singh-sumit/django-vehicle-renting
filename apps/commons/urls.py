from django.urls import path
from .views import (HomeView, CustomerRegisterView, OwnerRegisterView, OwnerLoginView, SystemAdminLoginView,
                    SystemAdminHomeView, UserLogoutView, AddCSRView, CSRLoginView, CSRHomeView, CSRPasswordUpdateView,
                    AddBoothManagerView, AddBoothView, BoothManagerLoginView, BoothManagerAddBikeView,
                    BoothManagerHomeView, BoothManagerPasswordUpdateView, BoothManagerAddCarView, CustomerLoginView,
                    MakeLicensedCustomerView, MakeReservationRequestView, ListPendingLicenseRequestView,
                    CSRCustomerDetailView, ManageLicenseRequestView)

app_name = 'commons'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    #################################################################################
    #                           Customer Part
    path('cust-signup/', CustomerRegisterView.as_view(), name="cust_signup"),
    path('cust-signin/', CustomerLoginView.as_view(), name="cust_signin"),
    path('cust-req-licensed/<int:pk>/', MakeLicensedCustomerView.as_view(), name="cust-req-licensed"),
    path('cust-req-reserv/', MakeReservationRequestView.as_view(), name="cust-req-reserv"),

    ###########################################################################
    #                   Vehicle Owner Part
    path('owner-signup/', OwnerRegisterView.as_view(), name='owner_signup'),
    path('owner-signin/', OwnerLoginView.as_view(), name='owner_signin'),

    ############################################################################
    #                   System Admin Part
    path('sys/', SystemAdminLoginView.as_view(), name="admin-signin"),
    path('sys/home/', SystemAdminHomeView.as_view(), name="admin-home"),
    path('sys/add-csr/', AddCSRView.as_view(), name="admin-add-csr"),

    ######################################################################3
    #                   CSR Part
    path('csr/', CSRLoginView.as_view(), name="csr-signin"),
    path('csr/home/', CSRHomeView.as_view(), name="csr-home"),
    path('csr/pwd-update/<int:pk>/', CSRPasswordUpdateView.as_view(), name="csr-pwd-update"),
    path('csr/booth-mngr/add/', AddBoothManagerView.as_view(), name="csr-add-bmngr"),
    path('csr/booth/add/', AddBoothView.as_view(), name="csr-add-booth"),
    path('csr/list-lic-req/', ListPendingLicenseRequestView.as_view(), name="csr-list-lic-req"),
    path('csr/cust-detail/<int:pk>/', CSRCustomerDetailView.as_view(), name="csr-cust-detail"),
    path('csr/manage-lic-req/<int:cid>/', ManageLicenseRequestView.as_view(), name="csr-manage-lic-req"),
    ###########################################################################
    #           Booth Manager Part
    path('bmgr/', BoothManagerLoginView.as_view(), name="bmgr-signin"),
    path('bmgr/home/', BoothManagerHomeView.as_view(), name="bmgr-home"),
    path('bmgr/pwd-update/<int:pk>/', BoothManagerPasswordUpdateView.as_view(), name="bmgr-pwd-update"),
    path('bmgr/add/bike/', BoothManagerAddBikeView.as_view(), name="bmgr-add-bike"),
    path('bmgr/add/car/', BoothManagerAddCarView.as_view(), name="bmgr-add-car"),

]
