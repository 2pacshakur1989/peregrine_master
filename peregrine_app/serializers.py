from rest_framework import serializers
from .models import Country,Flight

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['airline_company_id','origin_country_id','destination_country_id','departure_time','landing_time','remaining_tickets']
