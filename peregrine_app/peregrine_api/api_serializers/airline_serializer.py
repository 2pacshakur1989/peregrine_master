from rest_framework import serializers
from peregrine_app.models import AirlineCompany
from peregrine_app.peregrine_api.api_serializers.country_serializer import CountrySerializer
import re

class AirlineSerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()

    class Meta:
        model = AirlineCompany
        fields = ['name', 'country_id']


class AddAirlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirlineCompany
        fields = ['name', 'country_id']
