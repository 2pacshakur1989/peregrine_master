from rest_framework import serializers
from peregrine_app.models import Administrator


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name']
