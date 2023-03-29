from rest_framework import serializers
from peregrine_app.models import AirlineCompany
from peregrine_app.peregrine_api.api_serializers.country_serializer import CountrySerializer, AirlineCountrySerializer
import re

class AirlineSerializer(serializers.ModelSerializer):
    country_id = AirlineCountrySerializer()

    class Meta:
        model = AirlineCompany
        fields = ['id','name', 'country_id']


class AddAirlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirlineCompany
        fields = ['name', 'country_id']

    def validate(self, data):

        name = data.get('name')
        self.name_validation(name=name)
        return data
    
    def name_validation(self, name):

        name_pattern = re.compile(r'^[A-Za-z ]+$') # restrict to letters and spaces only
        if not re.fullmatch(name_pattern, name):
            raise serializers.ValidationError ('Names should contain only letters and spaces')
        elif len(name) < 3 or len(name) > 20:
            raise serializers.ValidationError ('Name should be between 3 and 20 characters long')


