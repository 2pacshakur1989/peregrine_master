from rest_framework import serializers
from peregrine_app.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','name']


class AirlineCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']




    