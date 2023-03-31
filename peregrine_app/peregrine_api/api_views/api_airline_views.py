"""Airline API , includes the GET,POST,PUT and DELETE methods, methods permissions vary from user to user"""
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.peregrine_api.api_serializers.airline_serializer import AirlineSerializer, AddAirlineSerializer
from peregrine_app.peregrine_api.api_serializers.user_serializer import UserSerializer
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.facades.airlinefacade import AirlineFacade
from peregrine_app.loggers import airline_logger


airlinefacade = AirlineFacade(user_group='airline')
adminfacade = AdministratorFacade(user_group='admin')

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def airline(request):


    # GET REQUESTS
    if request.method == 'GET':

        if 'country_id' in request.query_params:
            # Handle 'get_airlines_by_country' for all users
            country_id = request.query_params['country_id']
            airlines = airlinefacade.get_airline_by_country(request=request, country_id=country_id)
            serializer = AirlineSerializer(airlines, many=True)
            airline_logger.info('Get airline by country id Attempt')
            return Response(serializer.data)
        
        elif 'id' in request.query_params:
            # Handle 'get_airlines_by_id' for all users
            id = request.query_params['id']
            airline = airlinefacade.get_airline_by_id(request=request, id=id)
            serializer = AirlineSerializer(airline)
            airline_logger.info('Get airline by id Attempt')
            return Response(serializer.data)

        elif 'username' in request.query_params:  # For display the logged in airline 
            if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
                airline_logger.info('Unauthorized attempt')
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            airline_username = request.user.username
            username = request.query_params['username']
            airline = airlinefacade.get_airline_by_username(request=request, username=username, airline_username=airline_username)
            serializer = AirlineSerializer(airline)
            airline_logger.info('Get airline by username Attempt')
            return Response(serializer.data)
       
        else:
            airlines = airlinefacade.get_all_airlines(request=request)
            serializer = AirlineSerializer(airlines, many=True)
            airline_logger.info('Get all airlines Attempt')
            return Response(serializer.data)
        
    
    # POST REQUESTS
    if request.method == 'POST':
        # Validating the User
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            airline_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        # Serializing both the user details and the airline 
        user_serializer = UserSerializer(data=request.data)
        airline_serializer = AddAirlineSerializer(data=request.data)
        if not user_serializer.is_valid():
            airline_logger.error(user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        if not airline_serializer.is_valid():
            airline_logger.error(airline_serializer.errors)
            return Response(airline_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        adminfacade.add_airline(request=request, user_data=user_serializer.validated_data, data=airline_serializer.validated_data)
        airline_logger.info(f"Attempted add airline - airline {request.user.administrator.id}")
        return Response({"message": "Airline Created successfully","user_data":user_serializer.data ,"airline_data": airline_serializer.data}, status=status.HTTP_201_CREATED) 


    # PUT REQUESTS
    if request.method == 'PUT':
        # Validating the User
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
            airline_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if not 'id' in request.query_params:
            airline_logger.info('Airline id must be provided')
            return Response("Airline id must be provided.", status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.airlinecompany.id) != request.query_params['id']:
            airline_logger.info('Airline is allowed to update its own details ONLY')
            return Response("Airline is allowed to update its own details ONLY", status=status.HTTP_403_FORBIDDEN)  
        # Creating new serializer instances with the existing objects and partial=True (to allow the fields to be optional for update)
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        airline_serializer = AddAirlineSerializer(request.user.airlinecompany, data=request.data, partial=True)
        
        if not user_serializer.is_valid():
            airline_logger.error(user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not airline_serializer.is_valid():
            airline_logger.error(airline_serializer.errors)
            return Response(airline_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
        if airlinefacade.update_airline(request=request, airline_company_id=request.query_params['id'], user_id=request.user.id ,user_data=user_serializer.validated_data, data=airline_serializer.validated_data) is not None:
            airline_logger.info(f"Attempted update airline - airline {request.user.airlinecompany.id}")
            return Response({"message": "Airline Updated successfully","user_data":user_serializer.validated_data ,"airline_data": airline_serializer.validated_data}, status=status.HTTP_201_CREATED) 


    # DELETE REQUESTS
    if request.method == 'DELETE':
         # Validating the User - this action is permitted for the admin only
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            airline_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if not 'id' in request.query_params:
            airline_logger.info('Airline id must be provided')
            return Response("Airline id must be provided.", status=status.HTTP_400_BAD_REQUEST)
        airline_logger.error(f"Attempted remove airline - admin {request.user.administrator.id}")
        return Response (adminfacade.remove_airline(request=request, id=request.query_params['id']))

        
       
        
              