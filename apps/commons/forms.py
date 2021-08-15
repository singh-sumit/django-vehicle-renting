from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit
from django import forms
from django.forms import BaseModelForm, TextInput, IntegerField
from .models import (Customer, Owner, CSR, CustomerType)
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import (age, )
from ..vehicle_rental.models import BoothManager, Booth, Vehicle, Bike, Car


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

#####################################################################################
#               Make Licensed Customer Form
class MakeLicensedCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["license_doc"]


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

    def clean_username(self):
        return BaseUserRegisterationForm.clean_username(self)

    def clean_email(self):
        return BaseUserRegisterationForm.clean_email(self)


################################################################################
#           Base Password Update Form used by (CSR | Booth Manager)
class PasswordUpdateForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='New Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    def clean(self):
        upwd1 = self.cleaned_data.get('password1')
        upwd2 = self.cleaned_data.get('password2')
        # check if two password matched,and is of length > 8 , with proper characters (^,/,$,!,?)
        special_chars = ('/', '$', '!', '?')
        if (upwd1 != 'abcd1234') and (upwd1 == upwd2):
            if (len(upwd1) >= 8):
                if any((spc in upwd1) for spc in special_chars):
                    return upwd2
                else:
                    raise forms.ValidationError("Passwords must contain either of special chars ^,/,$,!,? ")
            else:
                raise forms.ValidationError("Password must be greater than 8")
        else:
            raise forms.ValidationError("Old Password Entered. Or, Password didn't matched.")


###############################################################################
#          Form for Adding Booth Manager to Office <-- CSR
class BoothManagerAddForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    # password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    # password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    perm_address = forms.CharField(label="Permanent Address", )
    curr_address = forms.CharField(label="Current Address", )

    class Meta:
        model = BoothManager
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile',
                  'perm_address', 'curr_address', ]

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
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('perm_address', css_class='form-group col-md-6 mb-0'),
                Column('curr_address', css_class='form-group col-md-6 mb-0', ),
                css_class='form-row'
            ),
            Submit('submit', "Add", css_class='btn btn-primary')
        )

    def clean_username(self):
        return BaseUserRegisterationForm.clean_username(self)

    def clean_email(self):
        return BaseUserRegisterationForm.clean_email(self)


#############################################################################
#           Form for adding Booth Office    <-- CSR
class AddBoothForm(forms.ModelForm):
    class Meta:
        model = Booth
        fields = "__all__"


############################################################################
#           Form for Adding Vehicle(Bike | Car)  <-- Booth Manager
class BaseAddVehicleForm(forms.ModelForm):
    # class Meta:
    #     model = Vehicle
    #     fields = ["plate_num", "owner", "fare", "brand", "mileage", "manufacturing_year"]
    #     exclude = ["wheels_num", "status", "issued_by", "residing_booth", "vehicle_type"]
    plate_num = forms.CharField(label="Plate Number", widget=forms.TextInput(),
                                help_text='Plate number like : BDE1234', max_length=7)
    fare = forms.CharField(widget=forms.NumberInput(), help_text='Enter a fare for per day')
    brand = forms.CharField(widget=forms.TextInput())
    mileage = forms.DecimalField()
    manufacturing_year = forms.CharField(max_length=4, widget=forms.NumberInput())
    seats = forms.CharField(widget=TextInput(), )
    qs = tuple(Owner.objects.all().values_list("id", "user__username"))
    owner = forms.ChoiceField(choices=qs)
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('plate_num', css_class='form-group col-md-4 mb-0'),
                Column('brand', css_class='form-group col-md-4 mb-0'),
                Column('mileage', css_class='form-group col-md-2 mb-0'),
                Column('seats', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fare', css_class='form-group col-md-4 mb-0'),
                Column('manufacturing_year', css_class='form-group col-md-4 mb-0', ),
                Column('owner', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class="form-group"),
                css_class='form-row'
            ),
            Submit('submit', "Add", css_class='btn btn-primary mt-2')
        )

    #####################################################
    #           cleaning fields
    def clean_plate_num(self):
        pnum = self.cleaned_data.get('plate_num')
        # check for uniqueness of plate number
        if Vehicle.objects.filter(plate_num=pnum).exists():
            raise forms.ValidationError("Vehicle with plate number already exists.")
        return pnum

##############################################################################
#           Form for Adding Bike  <-- Booth Manager
class BoothManagerAddBikeForm(BaseAddVehicleForm):
    class Meta:
        model = Bike
        fields = ["seats", "image", "plate_num", "fare", "brand", "mileage", "manufacturing_year"]
        exclude = ["wheels_num", "status", "issued_by", "residing_booth", "vehicle_type"]

    seats = forms.CharField(widget=TextInput(attrs={'value': 2}), )

##############################################################################
#           Form for Adding Car  <-- Booth Manager
class BoothManagerAddCarForm(BaseAddVehicleForm):
    class Meta:
        model = Bike
        fields = ["seats", "image", "plate_num", "fare", "brand", "mileage", "manufacturing_year"]
        exclude = ["wheels_num", "status", "issued_by", "residing_booth", "vehicle_type"]

    seats = forms.CharField(widget=TextInput(attrs={'value': 4}), )

####################################################################################
#           Form for Searching Reserved Vehicle <-- Booth Manager
class BoothManagerSearchReservedVehicleForm(forms.Form):
    reservation_id = forms.CharField(widget=forms.NumberInput(), help_text="Reservation Id: like Reserve_ID4")
    cust_name = forms.CharField(max_length=40,required=False,label="Customer Name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('reservation_id', css_class='form-group '),
                Column('cust_name', css_class='form-group ',),
                css_class='form-row'
            ),
        )


