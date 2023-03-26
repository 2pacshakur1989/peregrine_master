from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Country(models.Model):
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"


class Administrator(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class AirlineCompany(models.Model):

    name = models.CharField(max_length=255, unique=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    user_id =  models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Airline companies"


class Customer(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255, unique=True)
    credit_card_no = models.CharField(max_length=255, unique=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

class Flight(models.Model):

    airline_company_id = models.ForeignKey(AirlineCompany,on_delete=models.CASCADE)
    origin_country_id = models.ForeignKey(Country,on_delete=models.CASCADE,related_name='origin_flights')
    destination_country_id = models.ForeignKey(Country,on_delete=models.CASCADE, related_name='destination_flights')
    departure_time = models.DateTimeField()
    landing_time = models.DateTimeField()
    remaining_tickets = models.IntegerField()




class Ticket(models.Model):

    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)



