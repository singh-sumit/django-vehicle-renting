from django.urls import path
from .views import (HomeView, CustomerRegisterView, OwnerRegisterView, OwnerLoginView, SystemAdminLoginView,
                    SystemAdminHomeView, UserLogoutView, AddCSRView, CSRLoginView, CSRHomeView, CSRPasswordUpdateView,
                    AddBoothManagerView, AddBoothView, BoothManagerLoginView, BoothManagerAddBikeView,
                    BoothManagerHomeView,BoothManagerPasswordUpdateView, BoothManagerAddCarView)

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
    path('sys/add-csr/', AddCSRView.as_view(), name="admin-add-csr"),

    ######################################################################3
    #                   CSR Part
    path('csr/', CSRLoginView.as_view(), name="csr-signin"),
    path('csr/home/', CSRHomeView.as_view(), name="csr-home"),
    path('csr/pwd-update/<int:pk>/', CSRPasswordUpdateView.as_view(), name="csr-pwd-update"),
    path('csr/booth-mngr/add/', AddBoothManagerView.as_view(), name="csr-add-bmngr"),
    path('csr/booth/add/', AddBoothView.as_view(), name="csr-add-booth"),

    ###########################################################################
    #           Booth Manager Part
    path('bmgr/', BoothManagerLoginView.as_view(), name="bmgr-signin"),
    path('bmgr/home/', BoothManagerHomeView.as_view(), name="bmgr-home"),
    path('bmgr/pwd-update/<int:pk>/', BoothManagerPasswordUpdateView.as_view(), name="bmgr-pwd-update"),
    path('bmgr/add/bike/', BoothManagerAddBikeView.as_view(), name="bmgr-add-bike"),
    path('bmgr/add/car/', BoothManagerAddCarView.as_view(), name="bmgr-add-car"),

]
