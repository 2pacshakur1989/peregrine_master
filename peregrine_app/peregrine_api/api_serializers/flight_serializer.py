from rest_framework import serializers
from peregrine_app.models import Country,Flight

# class FlightSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Flight
#         fields = ['airline_company_id','origin_country_id','destination_country_id','departure_time','landing_time','remaining_tickets']





class FlightSerializer(serializers.ModelSerializer):
    airline_company = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = ['airline_company_id','origin_country_id','destination_country_id','departure_time','landing_time','remaining_tickets']

    def get_airline_company(self, obj):
        request = self.context.get('request')
        if request.user.groups.filter(name='airline').exists():
            return request.user.airlinecompany.name
        return obj.airline_company.name

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.groups.filter(name='airline').exists():
            airline_company = request.user.airlinecompany
            validated_data['airline_company'] = airline_company
            return super().create(validated_data)
        raise serializers.ValidationError("You don't have the permission to add a new flight.")

    def validate_airline_company(self, value):
        request = self.context.get('request')
        if request.user.groups.filter(name='airline').exists() and request.user.airlinecompany != value:
            raise serializers.ValidationError("You can only create flights for your airline company.")
        return value
