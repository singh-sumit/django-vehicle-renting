from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import (TemplateView, CreateView)
from .forms import (CustomerRegisterationForm)
from .models import (Customer, )
from django.utils import timezone


# Create your views here.
#################################################################
#               Customer HomeView
class HomeView(TemplateView):
    template_name = "home.html"


################################################################
#               Customer Register View
class CustomerRegisterView(CreateView):
    template_name = 'auth/register.html'
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
                                           curr_address=curr_address,mobile=mobile)

        # make user login to system
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)
