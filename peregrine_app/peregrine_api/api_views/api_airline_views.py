"""Airline API , includes the GET,POST,PUT and DELETE methods, methods permissions vary from user to user"""
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.peregrine_api.api_serializers.airline_serializer import AirlineSerializer, AddAirlineSerializer
from peregrine_app.peregrine_api.api_serializers.user_serializer import UserSerializer
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.facades.airlinefacade import AirlineFacade


airlinefacade = AirlineFacade(user_group='airline')
adminfacade = AdministratorFacade(user_group='admin')

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def airline(request, id=None):


    # GET REQUESTS
    if request.method == 'GET':

        if 'country_id' in request.query_params:
            # Handle 'get_airlines_by_country' for all users
            country_id = request.query_params['country_id']
            airlines = airlinefacade.get_airline_by_country(country_id=country_id)
            serializer = AirlineSerializer(airlines, many=True)
            return Response(serializer.data)
        
        elif 'id' in request.query_params:
            # Handle 'get_airlines_by_id' for all users
            id = request.query_params['id']
            airline = airlinefacade.get_airline_by_id(id=id)
            serializer = AirlineSerializer(airline)
            return Response(serializer.data)

        elif 'username' in request.query_params:  # For display the logged in airline 
            if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            airline_username = request.user.username
            username = request.query_params['username']
            airline = airlinefacade.get_airline_by_username(username=username, airline_username=airline_username)
            serializer = AirlineSerializer(airline)
            return Response(serializer.data)
       
        else:
            airlines = airlinefacade.get_all_airlines()
            serializer = AirlineSerializer(airlines, many=True)
            return Response(serializer.data)
        
    
    # POST REQUESTS
    if request.method == 'POST':
        # Validating the User
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        # Serializing both the user details and the airline 
        user_serializer = UserSerializer(data=request.data)
        airline_serializer = AddAirlineSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        if not airline_serializer.is_valid():
            return Response(airline_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        adminfacade.add_airline(request=request, user_data=user_serializer.validated_data, data=airline_serializer.validated_data)
        return Response({"message": "Airline Created successfully","user_data":user_serializer.data ,"airline_data": airline_serializer.data}, status=status.HTTP_201_CREATED) 


    # PUT REQUESTS
    if request.method == 'PUT':
        # Validating the User
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if str(request.user.airlinecompany.id) != id:
            return Response("Airline is allowed to update its own details ONLY", status=status.HTTP_403_FORBIDDEN)  
        # Creating new serializer instances with the existing objects and partial=True (to allow the fields to be optional for update)
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        airline_serializer = AddAirlineSerializer(request.user.airlinecompany, data=request.data, partial=True)
        
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not airline_serializer.is_valid():
            return Response(airline_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
       
        airlinefacade.update_airline(request=request, airline_company_id=id, user_id=request.user.id ,user_data=user_serializer.validated_data, data=airline_serializer.validated_data)
        return Response({"message": "Airline Updated successfully","user_data":user_serializer.validated_data ,"airline_data": airline_serializer.validated_data}, status=status.HTTP_201_CREATED) 


    # DELETE REQUESTS
    if request.method == 'DELETE':
         # Validating the User - this action is permitted for the admin only
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        return Response (adminfacade.remove_airline(request=request, id=id))

        
       
        
              