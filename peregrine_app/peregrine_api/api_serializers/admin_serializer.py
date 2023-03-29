from rest_framework import serializers
from peregrine_app.models import Administrator
import re


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name']

    def validate(self, data):

        first_name = data.get('first_name')
        self.name_validation(name=first_name)

        last_name = data.get('last_name')
        self.name_validation(name=last_name)
        
        return data
    
    def name_validation(self, name):

        name_pattern = re.compile(r'^[A-Za-z ]+$') # restrict to letters and spaces only
        if not re.fullmatch(name_pattern, name):
            raise serializers.ValidationError ('Names should contain only letters and spaces')
        elif len(name) < 3 or len(name) > 20:
            raise serializers.ValidationError ('Name should be between 3 and 20 characters long')