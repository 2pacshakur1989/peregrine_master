""" Flight serializer includes the built in serializers and my custom methods for validating"""

from rest_framework import serializers
from peregrine_app.models import Flight
from .country_serializer import CountrySerializer
from peregrine_app.facades.facadebase import FacadeBase
from datetime import datetime, timedelta
import pytz
facade = FacadeBase()

class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ['airline_company_id','origin_country_id','destination_country_id',
                'departure_time','landing_time','remaining_tickets']
   
    #Main method that executes all custom validation methods
    def validate(self, data):
        # Returning the output of the custom methods
        instance = self.instance
        # If updating an existing instance, use the existing values for fields not being updated
        if instance is not None:
            for field in self.Meta.fields:
                if field not in data:
                    data[field] = getattr(instance, field)


        oc_object = data.get('origin_country_id')
        dc_object = data.get('destination_country_id')  
        # Executing the function
        self.check_similar_countries(oc_id=oc_object.id, dc_id=dc_object.id)


        departure_time = data.get('departure_time')
        landing_time = data.get('landing_time')
        # Executing the function
        self.check_time_conflict(departure_time=departure_time,landing_time=landing_time)

        # Executing the function
        self.check_remaining_tickets(data.get('remaining_tickets'))

        return data

    # Makes sure the departure country and landing country aren't the same
    def check_similar_countries(self, oc_id, dc_id):

        if oc_id == dc_id:
            raise serializers.ValidationError('Origin and destination countries cannot be the same.')
        
    # Making sure the time flights make sense (for example making sure the departure time cannot be in the past)
    def check_time_conflict(self, departure_time, landing_time):
            
        current_time = datetime.now()
        twelve_hours_from_now = current_time + timedelta(hours=12)
        departure_time = departure_time.astimezone(pytz.UTC).replace(tzinfo=None)
        landing_time = landing_time.astimezone(pytz.UTC).replace(tzinfo=None)

        current_time = current_time.replace(second=0, microsecond=0)
        if departure_time < twelve_hours_from_now:
            raise serializers.ValidationError ('Departure time must be minimum 12 hours from now') 
        if not ((landing_time>(departure_time+timedelta(hours=2))) and (landing_time<(departure_time+timedelta(hours=18)))):
            raise serializers.ValidationError ('Landing time has to be 2-18 hours difference from departure time')
        if landing_time <= departure_time:
            raise serializers.ValidationError ('Landing time cannot be prior or equal to the departure time')
                           
    # Making sure the remaining tickets is of a real flight
    def check_remaining_tickets(self, remaining_tickets):
            
            if remaining_tickets < 300 or remaining_tickets >850:
                raise serializers.ValidationError ('300-850 tickets are allowed')
            
        

class DisplayFlightSerializer(serializers.ModelSerializer):

    airline_company_name = serializers.CharField(source='airline_company_id.name')
    origin_country_name = serializers.CharField(source='origin_country_id.name')
    destination_country_name = serializers.CharField(source='destination_country_id.name')

    class Meta:
        model = Flight
        fields = ['airline_company_name', 'origin_country_name',
                 'destination_country_name', 'departure_time', 'landing_time',
                  'remaining_tickets']
        



# class FlightSerializer(serializers.ModelSerializer):

#     origin_country_name = serializers.CharField(source='origin_country_id.name')
#     destination_country_name = serializers.CharField(source='destination_country_id.name')

#     class Meta:
#         model = Flight
#         fields = ['airline_company_id','origin_country_name',
#                  'destination_country_name','departure_time','landing_time','remaining_tickets']
   
#     #Main method that executes all custom validation methods
#     def validate(self, data):
#         # Returning the output of the custom methods

#         instance = self.instance
#         # If updating an existing instance, use the existing values for fields not being updated
#         if instance is not None:
#             for field in self.Meta.fields:
#                 if field not in data:
#                     data[field] = getattr(instance, field)

#         if data.get('origin_country_name'):
#             oc_object = data.get('origin_country_name')

#         if data.get('destination_country_name'):
#             dc_object = data.get('destination_country_name')  
#         # Executing the function
#         self.check_similar_countries(oc_id=oc_object, dc_id=dc_object)

#         if data.get('departure_time'):
#             departure_time = data.get('departure_time')

#         if data.get('landing_time'):
#             landing_time = data.get('landing_time')
#         # Executing the function
#         self.check_time_conflict(departure_time=departure_time,landing_time=landing_time)

#         if data.get('remaining_tickets'):
#             # Executing the function
#             self.check_remaining_tickets(data.get('remaining_tickets'))

#         return data

#     # Makes sure the departure country and landing country aren't the same
#     def check_similar_countries(self, oc_id, dc_id):

#         if oc_id == dc_id:
#             raise serializers.ValidationError('Origin and destination countries cannot be the same.')
        
#     # Making sure the time flights make sense (for example making sure the departure time cannot be in the past)
#     def check_time_conflict(self, departure_time, landing_time):
            
#         current_time = datetime.now()
#         twelve_hours_from_now = current_time + timedelta(hours=12)
#         departure_time = departure_time.astimezone(pytz.UTC).replace(tzinfo=None)
#         landing_time = landing_time.astimezone(pytz.UTC).replace(tzinfo=None)

#         current_time = current_time.replace(second=0, microsecond=0)
#         if departure_time < twelve_hours_from_now:
#             raise serializers.ValidationError ('Departure time must be minimum 12 hours from now') 
#         if not ((landing_time>(departure_time+timedelta(hours=2))) and (landing_time<(departure_time+timedelta(hours=18)))):
#             raise serializers.ValidationError ('Landing time has to be 2-18 hours difference from departure time')
#         if landing_time <= departure_time:
#             raise serializers.ValidationError ('Landing time cannot be prior or equal to the departure time')
                           
#     # Making sure the remaining tickets is of a real flight
#     def check_remaining_tickets(self, remaining_tickets):
            
#             if remaining_tickets < 300 or remaining_tickets >850:
#                 raise serializers.ValidationError ('300-850 tickets are allowed')







