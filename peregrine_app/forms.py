from django import forms
from .models import Customer , AirlineCompany, Flight , Country , Administrator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeInput
from datetime import timedelta,datetime
import pytz

import re


class LoginForm(forms.Form):
    
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)



class UserProfile(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):

        super(UserProfile, self).clean()

        # Username Validation
        username = self.cleaned_data.get('username')
        username = str(username) # Avoiding whitespaces

        username_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$')
        if not re.fullmatch(username_pattern, username):
            self.add_error('username', 'Username should contain English letters and numbers only')

        elif len(username) < 8 or len(username) > 20:
            self.add_error('username', 'Username should be between 8-20 characters')

        # Email Validation
        email = self.cleaned_data.get('email')
        email = str(email) # Avoiding whitespaces

        email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
        if not re.fullmatch(email_pattern, email):
            self.add_error('email', 'Email is not valid')

        # Password Validation
        password1 = self.cleaned_data.get('password1')
        password1 = str(password1)

        password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$')
        if not re.fullmatch(password_pattern, password1):
            self.add_error('password1', 'Password must contain english letters and numbers')

        elif len(password1) < 8 or len(password1) > 31:
            self.add_error('password1', 'Password should be between 8-30 characters')

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','email']  



class AddCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'phone_no', 'credit_card_no']
    
    def clean(self):

        super(AddCustomerForm, self).clean()

        # First name validation
        first_name = self.cleaned_data.get('first_name')
        first_name = str(first_name) # Avoiding whitespaces

        name_pattern = re.compile(r'^[A-Za-z ]+$') # restrict to letters and spaces only
        if not re.fullmatch(name_pattern, first_name):
            self.add_error('first_name', 'Name should contain only letters and spaces')

        elif len(first_name) < 3 or len(first_name) > 20:
            self.add_error('first_name', 'Name should be between 3 and 20 characters long')

        # Last name validation
        last_name = self.cleaned_data.get('last_name')
        last_name = str(last_name) # Avoiding whitespaces
       
        name_pattern = re.compile(r'^[A-Za-z ]+$') # restrict to letters and spaces only
        if not re.fullmatch(name_pattern, last_name):
            self.add_error('last_name', 'Name should contain only letters and spaces')

        elif len(last_name) < 3 or len(last_name) > 20:
            self.add_error('last_name', 'Name should be between 3 and 20 characters long')

        # Address Validation
        address = self.cleaned_data.get('address')
        address = str(address) # Avoiding whitespaces

        address_pattern = re.compile(r'^(?=.*[A-Za-z .])(?=.*\d)[A-Za-z\d]+$')
        if not re.fullmatch(address_pattern, address):
            self.add_error('address', 'Address should contain letters, spaces, numbers and dots')

        elif len(address) < 5 or len(address) > 20:
            self.add_error('address', 'Address should be between 5 and 20 characters long')

        # Phone No. Validation
        phone_no = self.cleaned_data.get('phone_no')
        phone_no = str(phone_no) # Avoiding whitespaces

        phone_pattern = re.compile(r'^[0-9]+$')
        if not re.fullmatch(phone_pattern, phone_no):
            self.add_error('phone_no', 'Phone should contain numbers only')

        elif len(phone_no) < 9 or len(phone_no) >20:
            self.add_error('phone_no', 'Phone number should be 9-20 numbers long')

        # Credit Card Validation
        credit_card_no = self.cleaned_data.get('credit_card_no')
        credit_card_no = str(credit_card_no)

        ccn_pattern = re.compile(r'^[\d\-]+$')
        if not re.fullmatch(ccn_pattern, credit_card_no):
            self.add_error('credit_card_no', 'Credit card is not valid, Please use numbers and ,-, only')

        elif len(credit_card_no) < 10 or len(credit_card_no) >20:
            self.add_error('credit_card_no', 'Credit card number should be between 10-20 characters long')

class UpdateCustomerForm(AddCustomerForm,forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'phone_no', 'credit_card_no']



class AddAirlineForm(forms.ModelForm):

    class Meta:
        model = AirlineCompany
        fields = ['name' , 'country_id']
    
    def clean(self):

        super(AddAirlineForm, self).clean()

        # Name Validation
        name = self.cleaned_data.get('name')
        name = str(name) # Avoiding whitespaces

        name_pattern = re.compile(r'^[A-Za-z-0-9]+$')
        if not re.fullmatch(name_pattern, name):
            self.add_error('name', 'Name should contain English letters and numbers only')

        elif len(name) < 4 or len(name) > 20:
            self.add_error('name', 'Name should be between 4-20 characters')

class UpdateAirlineForm(AddAirlineForm, forms.ModelForm):
    class Meta:
        model = AirlineCompany
        fields = ['name','country_id']



class AddAdminForm(forms.ModelForm):
    
    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name']

    def clean(self):

        super(AddAdminForm, self).clean()

        # Firstname Validation
        first_name = self.cleaned_data.get('first_name')
        first_name = str(first_name) # Avoiding whitespaces

        name_pattern = re.compile(r'^[A-Za-z]+$')
        if not re.fullmatch(name_pattern, first_name):
            self.add_error('first_name', 'Name should contain English letters only')

        elif len(first_name) < 3 or len(first_name) > 20:
            self.add_error('first_name', 'Name should be between 3-20 characters')

        # Lastname Validation
        last_name = self.cleaned_data.get('last_name')
        last_name = str(last_name) # Avoiding whitespaces

        name_pattern = re.compile(r'^[A-Za-z]+$')
        if not re.fullmatch(name_pattern, last_name):
            self.add_error('last_name', 'Name should contain English letters only')

        elif len(last_name) < 3 or len(last_name) > 20:
            self.add_error('last_name', 'Name should be between 3-20 characters')



class AddFlightForm(forms.ModelForm):

    departure_time = forms.DateTimeField(widget= DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    landing_time = forms.DateTimeField(widget= DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Flight
        fields = ['origin_country_id','destination_country_id','departure_time','landing_time','remaining_tickets']
    
    def clean(self):

        super(AddFlightForm, self).clean()

        # Countries Validation
        origin_country_id = self.cleaned_data.get('origin_country_id')
        destination_country_id = self.cleaned_data.get('destination_country_id')
        if origin_country_id == destination_country_id:
            self.add_error('destination_country_id', 'Origin and Destination countries cannot be the same')

        # Departure/Landing time Validation
        departure_time = self.cleaned_data.get('departure_time')
        departure_time = departure_time.astimezone(pytz.UTC).replace(tzinfo=None)
        landing_time = self.cleaned_data.get('landing_time')
        landing_time = landing_time.astimezone(pytz.UTC).replace(tzinfo=None)

        current_time = datetime.now()

        current_time = current_time.replace(second=0, microsecond=0)
        # print(current_time)
        twelve_hours_from_now = current_time + timedelta(hours=12)
        # twelve_hours_from_now = pytz.UTC.localize(twelve_hours_from_now)
        if departure_time == landing_time:
            print(True)
        else: 
            print(False)
        print(type(departure_time))
        print(landing_time)
        print(type(twelve_hours_from_now))
        if departure_time < twelve_hours_from_now:
            self.add_error('departure_time', 'departure time must be minimum 12 hours from now') 
        if not (landing_time>(departure_time+timedelta(hours=2))) and  (landing_time<(departure_time+timedelta(hours=18)))  :
            self.add_error('landing_time', 'Landing time has to be 2-18 hours difference from departure time') 
        if landing_time <= departure_time:
            self.add_error('landing_time', 'Landing time cannot be prior or equal to the departure time')               

        # Name Validation
        remaining_tickets = self.cleaned_data.get('remaining_tickets')

        if remaining_tickets < 300 or remaining_tickets >850:
            self.add_error('remaining_tickets', '300-850 tickets are allowed')            

class UpdateFlightForm(AddFlightForm, forms.ModelForm):

    departure_time = forms.DateTimeField(widget= DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    landing_time = forms.DateTimeField(widget= DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Flight
        fields = ['origin_country_id','destination_country_id','departure_time','landing_time','remaining_tickets']



class FlightFilterForm(forms.Form):

    origin_country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Origin Country", required=False)
    destination_country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Destination Country", required=False)
    departure_date = forms.DateTimeField(required=False, label='Departure Date', input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    landing_date = forms.DateTimeField(required=False, label='Landing Date', input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    airline_company = forms.ModelChoiceField(queryset=AirlineCompany.objects.all(), empty_label="Select Airline", required=False)

class AirlineFilterForm(forms.Form):

    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Origin Country", required=False)

class UserFilterForm(forms.Form):
    user_type = forms.ChoiceField(choices=(('customers', 'customers'), ('airlines', 'airlines'), ('admins', 'admins')))








