from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit
from django import forms
from .models import (Customer)
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import (age, )


########################################################################3
#                   Customer Registeration Form
class CustomerRegisterationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    perm_address = forms.CharField(label="Permanent Address",)
    curr_address = forms.CharField(label="Current Address",)

    dob = forms.DateField(label="Birth Date",
                          widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'dob',
                  'mobile', 'perm_address', 'curr_address']

    def __init__(self, *args, **kwargs):
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
                Column('curr_address', css_class='form-group col-md-6 mb-0',),
                css_class='form-row'
            ),
            Row(
                Column('dob', css_class='form-group col-md-6 mb-0'),
                Column('mobile', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Sign Up', css_class='btn btn-primary')
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

    def clean_dob(self):
        udob = self.cleaned_data.get('dob')
        if age(udob) < 18:
            raise forms.ValidationError("Your age must be greater than 18 years.")
        return udob
