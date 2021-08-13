from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.generic import (TemplateView, CreateView, FormView, View, UpdateView, ListView)
from .forms import (CustomerRegisterationForm, OwnerRegisterationForm, UserLoginForm, CSRRegistrationForm,
                    PasswordUpdateForm, BoothManagerAddForm, AddBoothForm, BoothManagerAddBikeForm,
                    BoothManagerAddCarForm, MakeLicensedCustomerForm, )
from .models import (Customer, Owner, Admin, CSR, Notification, CustomerType)
from django.utils import timezone
from ..vehicle_rental.models import BoothManager, Bike, Car, Vehicle


# Create your views here.
#################################################################
#               Customer HomeView
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add vehicles objects to context
        context['vehicle_lists'] = Vehicle.objects.filter(status="AVAILABLE")
        """
        [
            {'name':'bike','count':12},
            {'name':'car','count':4}
        ]
        """
        vehicles = [Car, Bike]
        context['available_vehicles'] = [
            {'name': veh.__name__, 'count': veh.objects.filter(vehicle__status="AVAILABLE").count()}
            for veh in vehicles
        ]

        # add notifications to context
        if (self.request.user.is_authenticated) and (self.request.user.customer):
            notifications = Notification.objects.filter(user__id=self.request.user.id)
            context['notifications'] = notifications.order_by("-id")[:5]
            context['notifications_count'] = len(notifications)
        return context


###########################################################################
#           Logout Customer, Owner, CSR, Admin
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("commons:home")


################################################################
#               Customer Register View
class CustomerRegisterView(CreateView):
    template_name = 'auth/register/customer.html'
    form_class = CustomerRegisterationForm
    success_url = reverse_lazy('commons:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        dob = form.cleaned_data.get('dob')
        perm_address = form.cleaned_data.get('perm_address')
        curr_address = form.cleaned_data.get('curr_address')
        mobile = form.cleaned_data.get('mobile')

        # Create user instance
        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name.title(), last_name=last_name.title(),
                                        email=email, last_login=timezone.now())

        # Create customer instance from user object
        customer = Customer.objects.create(user=user, dob=dob, perm_address=perm_address,
                                           curr_address=curr_address, mobile=mobile)

        # make user login to system
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)


###############################################################
#            Register As Licensed Customer
class MakeLicensedCustomerView(UpdateView):
    template_name = "customer/req_for_licensed.html"
    form_class = MakeLicensedCustomerForm
    success_url = reverse_lazy('commons:home')

    def get_queryset(self):
        cid = self.kwargs['pk']
        qs = Customer.objects.all()
        return qs

    def form_valid(self, form):
        # save license doc to db
        license_doc = form.cleaned_data.get("license_doc")
        customer = self.request.user.customer

        # rename as "license_<customer_id>.<ext>"
        if license_doc:
            license_doc.name = "license_{}_{}.{}".format(self.request.user.username, self.request.user.customer.id,
                                                         license_doc.name.split('.')[-1])
            customer.license_doc = license_doc
            customer.save()

            # Make notification for customer
            customer.user.notification_set.create(
                message="It requires some time to validate your request; for being licensed customer.")

            # Send notification for all CSR
            csrs = CSR.objects.all()
            for csr in csrs:
                csr.user.notification_set.create(message="Licensing Request Pending.")
        else:
            # save form while clearing existing photo
            form.save()

        # Make customer to redirect to its home
        return redirect(self.success_url, {})

    def form_invalid(self, form):
        return super().form_invalid(form)


################################################################
#           Licensed Customer Mixin
class LicensedRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        # check if customer is logined and is licensed
        if (request.user.is_authenticated) and (Customer.objects.filter(user=request.user).exists):
            try:
                request.user.customer.customertype.licensed
                return super().dispatch(request, *args, **kwargs)
            except Exception as e:
                print("My error >>>", e)
        # not logined user
        return redirect("commons:cust-req-licensed", pk=request.user.customer.id)


#############################################################################
#               Customer Makes Reservation Request
class MakeReservationRequestView(LicensedRequiredMixin, TemplateView):
    pass


###############################################################
#              Customer Login View
class CustomerLoginView(FormView):
    template_name = 'auth/login/customer.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('commons:home')

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pwd = form.cleaned_data.get('password')

        # authenticate user
        usr = authenticate(username=uname, password=pwd)

        if (usr is not None) and (Customer.objects.filter(user=usr).exists()):
            login(self.request, usr)
        else:
            return render(self.request, self.template_name,
                          {'form': form, 'error': 'Invalid Credentails'})
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': 'Invalid Credentials.'})


################################################################
#               Owner Register View
class OwnerRegisterView(CreateView):
    template_name = 'auth/register/owner.html'
    form_class = OwnerRegisterationForm
    success_url = reverse_lazy('commons:home')

    # saving to db if form data is valid
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')

        perm_address = form.cleaned_data.get('perm_address')
        curr_address = form.cleaned_data.get('curr_address')
        mobile = form.cleaned_data.get('mobile')

        # creating user instance
        user = User.objects.create_user(username=username, password=password, first_name=first_name.title(),
                                        last_name=last_name.title(), email=email, last_login=timezone.now())
        # creating Owner instance
        owner = Owner.objects.create(user=user, perm_address=perm_address, curr_address=curr_address,
                                     mobile=mobile)
        # make user to login to system
        login(self.request, user)
        return redirect(self.success_url)

    #
    def form_invalid(self, form):
        return super().form_invalid(form)


#################################################################
#           Owner Login View
class OwnerLoginView(FormView):
    template_name = 'auth/login/owner.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('commons:home')

    # check if form_valid and allow to login requested user
    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pwd = form.cleaned_data.get('password')

        # authenticate user
        usr = authenticate(username=uname, password=pwd)

        if (usr is not None) and (Owner.objects.filter(user=usr).exists()):
            login(self.request, usr)
        else:
            return render(self.request, self.template_name,
                          {'form': form, 'error': 'Invalid Credentails'})
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': 'Invalid Credentails'})


######################################################################
#           CSR Login View
class CSRLoginView(FormView):
    template_name = "auth/login/csr.html"
    form_class = UserLoginForm
    success_url = reverse_lazy('commons:csr-home')

    # check if form_valid and allow csr to its home page
    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pwd = form.cleaned_data.get('password')

        # authenticate user with uname and pwd
        usr = authenticate(username=uname, password=pwd)

        # check if logged in first time with default password
        if (usr is not None) and (CSR.objects.filter(user=usr).exists()):
            # make usr grant its login session
            login(self.request, usr)

            if (pwd == 'abcd1234'):
                # make csr to reset password
                return redirect(reverse_lazy('commons:csr-pwd-update', kwargs={'pk': usr.csr.id, }))
            else:
                # return csr to its home page
                return super().form_valid(form)
        else:
            # Credentials didn't matched
            return render(self.request, self.template_name,
                          {'form': form, 'error': 'Invalid Credentials. Try Again!!!'})

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': 'Invalid Credentials. Try Again!!!'})


######################################################################
#                   CSR Password Update View
class CSRPasswordUpdateView(FormView):
    template_name = "csr/update_pwd.html"
    form_class = PasswordUpdateForm
    success_url = reverse_lazy('commons:home')

    def form_valid(self, form):
        csrid = self.kwargs['pk']
        pwd = form.cleaned_data

        # save password to csr object
        csr = CSR.objects.get(id=csrid)
        csr.user.set_password(pwd)
        csr.user.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': 'Something is wrong.Please Try Again!!'})


#######################################################################
#                   CSR Home View
class CSRHomeView(TemplateView):
    template_name = "csr/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add notifications objects to context
        if (self.request.user.is_authenticated) and (self.request.user.csr):
            notifications = Notification.objects.filter(user__id=self.request.user.id)
            context['notifications'] = notifications
            context['notifications_count'] = len(notifications)
        # print(">>>>>>", context)
        return context


#######################################################################
#           Pending Licensing Request <-- CSR
class ListPendingLicenseRequestView(ListView):
    template_name = "csr/license_mgmt/base.html"

    def get_queryset(self):
        reqd_cust = list(CustomerType.objects.values_list('customer_id', flat=True))
        # exclude registered customer and (customer with license_doc=null)
        customers = Customer.objects.exclude(Q(id__in=reqd_cust) | Q(license_doc="") | Q(license_doc__isnull=True))
        return customers
        # print(">>>>>>>>>>",requesting_customer)
        # return requesting_customer


######################################################################
#           View Particular Customer detail     <-- CSR
class CSRCustomerDetailView(TemplateView):
    template_name = "csr/license_mgmt/check_for_verification.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        csid = kwargs.get('pk')
        context['cust'] = Customer.objects.get(id=csid)
        print(context)
        return context


#######################################################################
#        Manage LicenseRequest View   <-- CSR (Approve/Decline)
class ManageLicenseRequestView(View):

    def get(self, request, *args, **kwargs):
        csrid = self.request.user.csr.id
        cust_id = self.kwargs.get('cid')
        action = request.GET['action']
        cust = Customer.objects.get(id=cust_id)

        # either approve or decline
        if action == "aprov":
            CustomerType.objects.create(licensed=True, customer_id=cust_id, verifier_id=csrid)
            Notification.objects.create(user_id=cust.user.id,
                                        message="You are now a licensed Customer.Begin Reserving...")
        else:
            # decline
            cust.license_doc = None
            cust.save()
            Notification.objects.create(user_id=cust.user.id,
                                        message="Provide valid identity.Retry, Latter.")

        return redirect(reverse_lazy('commons:csr-list-lic-req'))


#######################################################################
#             Add Booth Office <-- CSR
class AddBoothView(CreateView):
    template_name = "csr/booth/add.html"
    form_class = AddBoothForm
    success_url = reverse_lazy('commons:csr-home')


#######################################################################
#             Add Booth Manager to Office <-- CSR
class AddBoothManagerView(CreateView):
    template_name = "csr/booth_manager/add.html"
    form_class = BoothManagerAddForm
    success_url = reverse_lazy('commons:csr-home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        perm_address = form.cleaned_data.get('perm_address')
        curr_address = form.cleaned_data.get('curr_address')
        mobile = form.cleaned_data.get('mobile')

        # Create user instance
        user = User.objects.create_user(username=username, password="abcd1234",
                                        first_name=first_name.title(), last_name=last_name.title(),
                                        email=email, last_login=timezone.now())

        # Create customer instance from user object
        booth_manager = BoothManager.objects.create(user=user, perm_address=perm_address,
                                                    curr_address=curr_address, mobile=mobile)

        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)


##########################################################################
#           Booth Manager Login
class BoothManagerLoginView(FormView):
    template_name = "auth/login/bmgr.html"
    form_class = UserLoginForm
    success_url = reverse_lazy('commons:bmgr-home')

    # check if form_valid and allow csr to its home page
    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pwd = form.cleaned_data.get('password')

        # authenticate user with uname and pwd
        usr = authenticate(username=uname, password=pwd)

        # check if logged in first time with default password
        if (usr is not None) and (BoothManager.objects.filter(user=usr).exists()):
            # make usr grant its login session
            login(self.request, usr)

            if (pwd == 'abcd1234'):
                # make csr to reset password
                return redirect(reverse_lazy('commons:bmgr-pwd-update', kwargs={'pk': usr.boothmanager.id, }))
            else:
                # return csr to its home page
                return super().form_valid(form)
        else:
            # Credentials didn't matched
            return render(self.request, self.template_name,
                          {'form': form, 'error': 'Invalid Credentials. Try Again!!!'})

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': 'Invalid Credentials. Try Again!!!'})


###########################################################################
#           Booth Manager Password Update View
class BoothManagerPasswordUpdateView(FormView):
    template_name = "bmgr/update_pwd.html"
    form_class = PasswordUpdateForm
    success_url = reverse_lazy('commons:home')

    def form_valid(self, form):
        bmgrid = self.kwargs['pk']
        pwd = form.cleaned_data

        # save password to csr object
        bmgr = BoothManager.objects.get(id=bmgrid)
        bmgr.user.set_password(pwd)
        bmgr.user.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': 'Something is wrong.Please Try Again!!'})


##########################################################################
#           Booth Manager Home View
class BoothManagerHomeView(TemplateView):
    template_name = "bmgr/home.html"


##########################################################################
#           Add Bike <-- BoothManager (in the name of Owner)
class BoothManagerAddBikeView(CreateView):
    template_name = "bmgr/vehicles/add_bike.html"
    form_class = BoothManagerAddBikeForm
    success_url = reverse_lazy('commons:bmgr-home')

    def form_valid(self, form):
        # exclude = ["wheels_num", "status", "issued_by", "residing_booth", "vehicle_type"]
        plate_num = form.cleaned_data.get('plate_num')
        oid = form.cleaned_data.get('owner')
        fare = form.cleaned_data.get('fare')
        seats = form.cleaned_data.get('seats')
        brand = form.cleaned_data.get('brand')
        mileage = form.cleaned_data.get('mileage')
        manufacturing_year = form.cleaned_data.get('manufacturing_year')
        image = form.cleaned_data.get('image')

        # change name of image to "bike<plate_num>.<ext>"
        image.name = "bike_{}.{}".format(plate_num, image.name.split('.')[-1])

        boothmanager = self.request.user.boothmanager
        booth = boothmanager.booth

        # create vehicle instance
        vehicle = Vehicle.objects.create(plate_num=plate_num, fare=fare, brand=brand, mileage=mileage,
                                         manufacturing_year=manufacturing_year, owner_id=oid, issuer=boothmanager,
                                         residing_booth=booth)
        bike = Bike.objects.create(vehicle=vehicle, seats=seats, image=image, )
        return redirect(self.success_url, {})

    def form_invalid(self, form):
        return super().form_invalid(form)


##########################################################################
#           Add Car <-- BoothManager (in the name of Owner)
class BoothManagerAddCarView(CreateView):
    template_name = "bmgr/vehicles/add_car.html"
    form_class = BoothManagerAddCarForm
    success_url = reverse_lazy('commons:bmgr-home')

    def form_valid(self, form):
        # exclude = ["wheels_num", "status", "issued_by", "residing_booth", "vehicle_type"]
        plate_num = form.cleaned_data.get('plate_num')
        oid = form.cleaned_data.get('owner')
        fare = form.cleaned_data.get('fare')
        seats = form.cleaned_data.get('seats')
        brand = form.cleaned_data.get('brand')
        mileage = form.cleaned_data.get('mileage')
        manufacturing_year = form.cleaned_data.get('manufacturing_year')
        image = form.cleaned_data.get('image')

        # change name of image to "bike<plate_num>.<ext>"
        image.name = "car_{}.{}".format(plate_num, image.name.split('.')[-1])

        boothmanager = self.request.user.boothmanager
        booth = boothmanager.booth

        # create vehicle instance
        vehicle = Vehicle.objects.create(plate_num=plate_num, fare=fare, brand=brand, mileage=mileage,
                                         manufacturing_year=manufacturing_year, owner_id=oid, issuer=boothmanager,
                                         residing_booth=booth)
        car = Car.objects.create(vehicle=vehicle, seats=seats, image=image, )
        return redirect(self.success_url, {})

    def form_invalid(self, form):
        return super().form_invalid(form)


########################################################################3
#           System Admin Home View
class SystemAdminHomeView(TemplateView):
    template_name = "sysadmin/home.html"


#########################################################################
#           System Admin Login View
class SystemAdminLoginView(FormView):
    template_name = "auth/login/admin.html"
    form_class = UserLoginForm
    success_url = reverse_lazy('commons:admin-home')

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pwd = form.cleaned_data.get('password')

        # authenticate user
        usr = authenticate(username=uname, password=pwd)

        if (usr is not None) and (Admin.objects.filter(user=usr).exists()):
            login(self.request, usr)
        else:
            return render(self.request, self.template_name,
                          {'form': form, 'error': 'Invalid Credentails'})
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': 'Invalid Credentails'})


########################################################################
#            Add CSR <-- System Admin
class AddCSRView(CreateView):
    template_name = "sysadmin/csr/add.html"
    success_url = reverse_lazy('commons:admin-home')
    form_class = CSRRegistrationForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        salary = form.cleaned_data.get('salary')
        perm_address = form.cleaned_data.get('perm_address')
        curr_address = form.cleaned_data.get('curr_address')
        mobile = form.cleaned_data.get('mobile')

        # Create user instance
        user = User.objects.create_user(username=username, password="abcd1234",
                                        first_name=first_name.title(), last_name=last_name.title(),
                                        email=email, last_login=timezone.now())

        # Create customer instance from user object
        csr = CSR.objects.create(user=user, salary=salary, perm_address=perm_address,
                                 curr_address=curr_address, mobile=mobile)

        # make user login to system
        # login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)
