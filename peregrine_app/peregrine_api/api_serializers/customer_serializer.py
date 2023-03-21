from rest_framework import serializers
from peregrine_app.models import Customer
import re

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'phone_no', 'credit_card_no']


    def validate(self, data):
        # Returning the output of the custom methods

        instance = self.instance
        # If updating an existing instance, use the existing values for fields not being updated
        if instance is not None:
            for field in self.Meta.fields:
                if field not in data:
                    data[field] = getattr(instance, field)

        if data.get('first_name'):
            first_name = data.get('first_name')

        if data.get('last_name'):   
            last_name = data.get('last_name')

        self.name_validation(first_name=first_name, last_name=last_name)
        
        if data.get('address'):
            address = data.get('address')
            self.address_validation(address=address)

        if data.get('phone_no'):
            phone_no = data.get('phone_no')
            self.phone_no_validation(phone_no=phone_no)

        if data.get('credit_card_no'):
            credit_card_no = data.get('credit_card_no')
            self.credit_card_validation(credit_card_no=credit_card_no)

        return data

    # def first_name_validation(self, first_name):

    #     name_pattern = re.compile(r'^[A-Za-z ]+$') # restrict to letters and spaces only
    #     if not re.fullmatch(name_pattern, first_name):
    #         raise serializers.ValidationError ('Names should contain only letters and spaces')

    #     elif len(first_name) < 3 or len(first_name) > 20:
    #         raise serializers.ValidationError ('Name should be between 3 and 20 characters long')
        
    # def last_name_validation(self, last_name):

    #     name_pattern = re.compile(r'^[A-Za-z ]+$') # restrict to letters and spaces only
    #     if not re.fullmatch(name_pattern, last_name):
    #         raise serializers.ValidationError ('Names should contain only letters and spaces')

    #     elif len(last_name) < 3 or len(last_name) > 20:
    #         raise serializers.ValidationError ('Name should be between 3 and 20 characters long')

    def name_validation(self, first_name, last_name):
        name_pattern = re.compile(r'^[A-Za-z ]+$') # restrict to letters and spaces only
        if (not re.fullmatch(name_pattern, first_name)) or (not re.fullmatch(name_pattern, last_name)):
            raise serializers.ValidationError ('Names should contain only letters and spaces')
        elif (len(first_name) < 3 or len(first_name) > 20) or (len(last_name) < 3 or len(last_name) > 20):
            raise serializers.ValidationError ('Name should be between 3 and 20 characters long')
           
         
    def address_validation(self, address):

        address_pattern = re.compile(r'^[A-Za-z\d]+[A-Za-z\d\s\.]*$')
        if not re.fullmatch(address_pattern, address):
            raise serializers.ValidationError ('Address MUST contain English letter and numbers')
        elif not ( 5 < len(address) < 25 ):
            raise serializers.ValidationError ('Address length must be between 5-25 characters')
        
    def phone_no_validation(self, phone_no):

        phone_pattern = re.compile(r'^\d+(-\d+)*$')
        if not re.fullmatch(phone_pattern, phone_no):
            raise serializers.ValidationError ('Phone number can contain numbers and -')
        elif not ( 6 < len(phone_no) < 12):
             raise serializers.ValidationError ('Phone number length should be 7-11 characters')
        
    def credit_card_validation(self, credit_card_no):

        credit_card_pattern = re.compile(r'^\d+(?:-\d+)+$')
        if not re.fullmatch(credit_card_pattern, credit_card_no):
            raise serializers.ValidationError ('Credit card number must contain numbers and -')        
        elif not ( 11 < len(credit_card_no) < 21):
             raise serializers.ValidationError ('Credit card number length should be 12-20 characters')         





