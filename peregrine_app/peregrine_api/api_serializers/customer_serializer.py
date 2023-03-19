from rest_framework import serializers
from peregrine_app.models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'phone_no', 'credit_card_no']


class CustomerRemoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'phone_no', 'credit_card_no', 'user_id']

