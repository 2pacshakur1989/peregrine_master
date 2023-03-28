from rest_framework import serializers
from peregrine_app.models import Ticket

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['flight_id', 'customer_id']