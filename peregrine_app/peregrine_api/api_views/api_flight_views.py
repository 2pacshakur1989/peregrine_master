"""This is the Flight API view, it has different GET options which are all available to the anonymous user.
The POST, PUT,DELETE methods are permitted for the Airline companies ONLY! """

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.peregrine_api.api_serializers.flight_serializer import FlightSerializer, DisplayFlightSerializer
from peregrine_app.facades.airlinefacade import AirlineFacade
from peregrine_app.loggers import flight_logger

airlinefacade = AirlineFacade(user_group='airline')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def flight(request):


    # GET REQUESTS
    if request.method == 'GET':

        if 'id' in request.query_params:
            # Handle 'get a specific flight' for other users
            id = request.query_params['id']
            flight = airlinefacade.get_flight_by_id(request=request, id=id)  
            serializer = DisplayFlightSerializer(flight)
            flight_logger.info('get flight by id attempt')
            return Response(serializer.data)
        
        if 'update' in request.query_params:
            # Handle 'get a specific flight' for other users
            id = request.query_params['update']
            flight = airlinefacade.get_flight_by_id(request=request, id=id)  
            serializer = FlightSerializer(flight)
            flight_logger.info('get flight by id attempt')
            return Response(serializer.data)
        
        elif 'my' in request.query_params:

            if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            # my = request.query_params['my']
            id = request.user.airlinecompany.id
            flights = airlinefacade.get_my_flights(request=request, airline_company_id=id)
            if flights is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = DisplayFlightSerializer(flights, many=True)
            flight_logger.info(f"Attempted get my flights - airline {request.user.airlinecompany.id}")
            return Response(serializer.data)
              
         
        # Get parameters from query params
    
        origin_country_id = request.query_params.get('origin_country_id')
        destination_country_id = request.query_params.get('destination_country_id')
        airline_company_id = request.query_params.get('airline_company_id')
        departure_time = request.query_params.get('departure_time')
        landing_time = request.query_params.get('landing_time')

        # Filter flights by parameters if they are provided
        flights = airlinefacade.get_flights_by_combined_parameters(request=request, origin_country_id=origin_country_id, destination_country_id=destination_country_id, airline_company_id=airline_company_id, departure_time=departure_time, landing_time=landing_time)
        # Serialize and return flights
        serializer = DisplayFlightSerializer(flights, many=True)
        flight_logger.info('Get flights by parameters attempt')
        return Response(serializer.data)
      
    
    #POST REQUESTS
    elif request.method == 'POST':
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
            flight_logger.info('Unauthorized attempted request')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        airlinecompany = request.user.airlinecompany
        serializer = FlightSerializer(data=request.data)       
        if serializer.is_valid():
            # Use validated data instead of request.data
            new_flight = airlinefacade.add_flight(request=request, data=serializer.validated_data, airlinecompany=airlinecompany)
            serializer = FlightSerializer(new_flight)
            flight_logger.info(f"Attempted Add flight - airline {request.user.airlinecompany.id}")
            # return Response({"message": "Flight Created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_200_OK)
        flight_logger.error(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # PUT REQUESTS
    elif request.method == 'PUT':
        if not ((request.user.is_authenticated) or (request.user.groups.filter(name='airline').exists())):
            flight_logger.info('Unauthorized attempted request')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)                
        airlinecompany = request.user.airlinecompany
 
        if not 'id' in request.query_params:
           return Response("Flight id must be provided.", status=status.HTTP_400_BAD_REQUEST)   
        serializer = FlightSerializer(data=request.data)       
        if serializer.is_valid():
            # Use validated data instead of request.data
            if airlinefacade.update_flight(request=request, data=serializer.validated_data, flight_id=request.query_params['id'], airlinecompany=airlinecompany) is not None:
                flight_logger.info(f"Attempted update flight - airline {request.user.airlinecompany.id}")
                return Response(status=status.HTTP_200_OK)
                # return Response({"message": "Flight Updated successfully", "data": serializer.validated_data}, status=status.HTTP_201_CREATED)
        flight_logger.error(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DELETE REQUESTS
    elif request.method == 'DELETE':
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())) :
            flight_logger.info('Unauthorized attempted request')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if not 'id' in request.query_params:
           flight_logger.info('Flight id must be provided')
           return Response("Flight id must be provided.", status=status.HTTP_400_BAD_REQUEST)   
        airlinecompany = request.user.airlinecompany  
        flight_logger.info(f"Attempted remove flight - airline {request.user.airlinecompany.id}")
        if airlinefacade.remove_flight(request=request, flight_id=request.query_params['id'] ,airlinecompany=airlinecompany) is not False:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)










