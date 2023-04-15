from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import re


class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

    # Main method that executes all custom validation methods    
    def validate(self, data):

        username = data.get('username')
        self.username_validation(username=username)

        email = data.get('email')
        self.email_validation(email=email)

        password1 = data.get('password1')
        password2 = data.get('password2')
        self.password_validation(password1=password1, password2=password2)
          
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
          




class UpdateUserSerializer(serializers.ModelSerializer):

    current_password = serializers.CharField(max_length=128, write_only=True, required=False)
    password1 = serializers.CharField(max_length=128, write_only=True, required=False)
    password2 = serializers.CharField(max_length=128, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'current_password', 'password1','password2']

    # Main method that executes all custom validation methods    
    def validate(self, data):

        username = data.get('username')
        self.username_validation(username=username)

        email = data.get('email')
        self.email_validation(email=email)

        current_password = data.get('current_password')
        password1 = data.get('password1')
        password2 = data.get('password2')
        self.password_validation(current_password=current_password, password1=password1, password2=password2)

        self.password_fields_validation(current_password=data.get('current_password'),
                                        password1=data.get('password1'),
                                        password2=data.get('password2')) 
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
        
    def password_validation(self, current_password, password1, password2):
        print(password1)
        if password1 is None:
            return
        password_pattern = re.compile(r'^[a-zA-Z0-9]+$')

        if not re.fullmatch(password_pattern, password1):
            if password1 is None:
                return
            raise serializers.ValidationError (""" The password must start with one or more alphanumeric characters.
This must be followed by zero or more additional alphanumeric characters.
The password cannot contain any other characters besides English letters (upper or lower) and numbers.""")
        elif not 7 < len(password1) < 31:
            raise serializers.ValidationError ('Password should be between 8-30 characters')
        elif password2 != password1 :
            raise serializers.ValidationError ('The passwords do not match')
        
    def password_fields_validation(self, current_password, password1, password2):
        if (current_password is not None) or (password1 is not None) or (password2 is not None):
            if (current_password is not None) and (password1 is not None) and (password2 is not None): 
                return
            else:
                raise serializers.ValidationError('Either all three password fields must be empty or all three must be provided with values')
        return # raise serializers.ValidationError('Either all three password fields must be empty or all three must be provided with values')
