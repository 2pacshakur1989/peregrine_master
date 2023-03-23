from rest_framework import serializers
from django.contrib.auth.models import User
import re


class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

    # Main method that executes all custom validation methods    
    def validate(self, data):

        if data.get('username'):
            username = data.get('username')
            self.username_validation(username=username)

        if data.get('email'):
            email = data.get('email')
            self.email_validation(email=email)

        if data.get('password1') or data.get('password2'):
            if data.get('password1') and data.get('password2'):
                password1 = data.get('password1')
                password2 = data.get('password2')
                self.password_validation(password1=password1, password2=password2)
            else:
                raise serializers.ValidationError ('In order to update a password, both the password field and the confirmation field are required')

        return data
    
    def username_validation(self, username):

        username_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$')
        if not re.fullmatch(username_pattern, username):
            raise serializers.ValidationError ('Username should contain English letters and numbers only')
        elif not 7 < len(username) < 21:
           raise serializers.ValidationError ('Username should be between 8-20 characters') 
        
    def email_validation(self, email):

        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not re.fullmatch(email_pattern, email):
            raise serializers.ValidationError ('Email is invalid')
        elif not 5 < len(email) < 41 : 
            raise serializers.ValidationError ('Email should be 6-40 characters in total')
        
    def password_validation(self, password1, password2):

        password_pattern = re.compile(r'^[a-zA-Z0-9]+$')
        if not re.fullmatch(password_pattern, password1):
            raise serializers.ValidationError (""" The password must start with one or more alphanumeric characters.
This must be followed by zero or more additional alphanumeric characters.
The password cannot contain any other characters besides English letters (upper or lower) and numbers.""")
        elif not 7 < len(password1) < 31:
            raise serializers.ValidationError ('Password should be between 8-30 characters')
        elif password2 != password1 :
            raise serializers.ValidationError ('The passwords do not match')
          

