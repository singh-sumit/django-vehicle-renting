from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.generic import (TemplateView, CreateView, FormView, View)
from .forms import (CustomerRegisterationForm, OwnerRegisterationForm, UserLoginForm, CSRRegistrationForm)
from .models import (Customer, Owner, Admin, CSR)
from django.utils import timezone


# Create your views here.
#################################################################
#               Customer HomeView
class HomeView(TemplateView):
    template_name = "home.html"

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
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                        last_name=last_name, email=email, last_login=timezone.now())
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

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': 'Invalid Credentials'})

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
        customer = CSR.objects.create(user=user, salary=salary, perm_address=perm_address,
                                           curr_address=curr_address, mobile=mobile)

        # make user login to system
        # login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)

