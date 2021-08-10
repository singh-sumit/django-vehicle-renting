from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit
from django import forms
from django.forms import BaseModelForm, TextInput

from .models import (Customer, Owner, CSR)
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import (age, )


########################################################################################
#               General User Login Form
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


########################################################################3
#                   Base User Registeration Form
class BaseUserRegisterationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    perm_address = forms.CharField(label="Permanent Address", )
    curr_address = forms.CharField(label="Current Address", )

    def __init__(self, *args, **kwargs):
        fields = kwargs['fields']
        del kwargs['fields']
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-4 mb-0'),
                Column('password1', css_class='form-group col-md-4 mb-0'),
                Column('password2', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('perm_address', css_class='form-group col-md-6 mb-0'),
                Column('curr_address', css_class='form-group col-md-6 mb-0', ),
                css_class='form-row'
            ),
            Row(
                Column('mobile', css_class='form-group col-md-6 mb-0'),
                Column('dob', css_class='form-group col-md-6 mb-0'),
                Column('salary', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', fields['submit_name'], css_class='btn btn-primary')
        )

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        # check if User with that username already exists
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Username already taken")
        return uname

    def clean_password2(self):
        upwd1 = self.cleaned_data.get('password1')
        upwd2 = self.cleaned_data.get('password2')
        # check if two password matched,and is of length > 8 , with proper characters (^,/,$,!,?)
        special_chars = ('/', '$', '!', '?')
        if (upwd1 == upwd2):
            if (len(upwd1) >= 8):
                if any((spc in upwd1) for spc in special_chars):
                    return upwd2
                else:
                    raise forms.ValidationError("Passwords must contain either of special chars ^,/,$,!,? ")
            else:
                raise forms.ValidationError("Password must be greater than 8")
        else:
            raise forms.ValidationError("Password didn't matched.")

    def clean_email(self):
        uemail = self.cleaned_data.get('email')
        # check if User with that email already exists
        if User.objects.filter(email=uemail).exists():
            raise forms.ValidationError("Customer with that email already exists.")
        return uemail


#####################################################################################
#                 Customer Registeration Form
class CustomerRegisterationForm(BaseUserRegisterationForm):
    dob = forms.DateField(label="Birth Date",
                          widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email',
                  'mobile', 'dob', 'perm_address', 'curr_address']

    def __init__(self, *args, **kwargs):
        fields = {'submit_name': 'Sign Up', }
        kwargs['fields'] = fields
        super().__init__(*args, **kwargs)

    #################################################################3
    #       Field Cleaning Operations
    def clean_dob(self):
        udob = self.cleaned_data.get('dob')
        if age(udob) < 18:
            raise forms.ValidationError("Your age must be greater than 18 years.")
        return udob


######################################################################################
#               Owner Registeration Form
class OwnerRegisterationForm(BaseUserRegisterationForm):
    class Meta:
        model = Owner
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email',
                  'mobile', 'perm_address', 'curr_address']

    def __init__(self, *args, **kwargs):
        fields = {'submit_name': 'Sign Up', }
        kwargs['fields'] = fields
        super().__init__(*args, **kwargs)


#####################################################################################3
#             CSR Registeration Form
class CSRRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    # password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    # password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    perm_address = forms.CharField(label="Permanent Address", )
    curr_address = forms.CharField(label="Current Address", )
    salary = forms.IntegerField()

    class Meta:
        model = CSR
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile',
                  'perm_address', 'curr_address', 'salary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-4 mb-0'),
                Column('mobile', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),
                Column('salary', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('perm_address', css_class='form-group col-md-6 mb-0'),
                Column('curr_address', css_class='form-group col-md-6 mb-0', ),
                css_class='form-row'
            ),
            Submit('submit', "Add", css_class='btn btn-primary')
        )
