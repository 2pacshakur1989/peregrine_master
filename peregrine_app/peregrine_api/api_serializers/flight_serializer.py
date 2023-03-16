from rest_framework import serializers
from peregrine_app.models import Country,Flight
from datetime import datetime, timedelta
import pytz

class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ['airline_company_id','origin_country_id','destination_country_id','departure_time','landing_time','remaining_tickets']


    def validate(self, data):
        # Returning the output of the custom methods
        self.check_similar_countries(data.get('origin_country_id'), data.get('destination_country_id'))
        self.check_time_conflict(data.get('departure_time'), data.get('landing_time'))
        self.check_remaining_tickets(data.get('remaining_tickets'))

        return data

    # Makes sure the departure country and landing country aren't the same
    def check_similar_countries(self, origin_country_id, destination_country_id):

        if origin_country_id == destination_country_id:
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
        if not (landing_time>(departure_time+timedelta(hours=2))) and (landing_time<(departure_time+timedelta(hours=18))):
            raise serializers.ValidationError ('Landing time has to be 2-18 hours difference from departure time')
        if landing_time <= departure_time:
            raise serializers.ValidationError ('Landing time cannot be prior or equal to the departure time')
                           
    # Making sure the remaining tickets is of a real flight
    def check_remaining_tickets(self, remaining_tickets):
            
            if remaining_tickets < 300 or remaining_tickets >850:
                raise serializers.ValidationError ('300-850 tickets are allowed')
            
            
         



# class FlightSerializer(serializers.ModelSerializer):
#     airline_company = serializers.SerializerMethodField()

#     class Meta:
#         model = Flight
#         fields = ['airline_company_id','origin_country_id','destination_country_id','departure_time','landing_time','remaining_tickets']

#     def get_airline_company(self, obj):
#         request = self.context.get('request')
#         if request.user.groups.filter(name='airline').exists():
#             return request.user.airlinecompany.name
#         return obj.airline_company.name

#     def create(self, validated_data):
#         request = self.context.get('request')
#         if request.user.groups.filter(name='airline').exists():
#             airline_company = request.user.airlinecompany
#             validated_data['airline_company'] = airline_company
#             return super().create(validated_data)
#         raise serializers.ValidationError("You don't have the permission to add a new flight.")

#     def validate_airline_company(self, value):
#         request = self.context.get('request')
#         if request.user.groups.filter(name='airline').exists() and request.user.airlinecompany != value:
#             raise serializers.ValidationError("You can only create flights for your airline company.")
#         return value



# class FlightDeleteSerializer(serializers.Serializer):
#     def delete(self, id):
#         airlinefacade.remove_flight(flight_id=id)
