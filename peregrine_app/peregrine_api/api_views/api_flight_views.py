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
        
        elif 'my' in request.query_params:

            if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            # my = request.query_params['my']
            id = request.user.airlinecompany.id
            flights = airlinefacade.get_my_flights(request=request, airline_company_id=id)
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
    



        # if 'origin' in request.query_params:
        #     # Handle 'get_flights_by_origin_country' for all users
        #     origin_country = request.query_params['origin']
        #     flights = airlinefacade.get_flights_by_origin_country_id(request=request, origin_country_id=origin_country)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info('Get flights by origin country attempt')
        #     return Response(serializer.data)
        
        # elif 'destination' in request.query_params:
        #     # Handle 'get_flights_by_destination_country' for all users
        #     destination_country = request.query_params['destination']
        #     flights = airlinefacade.get_flights_by_destination_country_id(request=request, destination_country_id=destination_country)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info('Get flights by destination country attempt')
        #     return Response(serializer.data)
        
        # elif 'airline' in request.query_params:
        #     # Handle 'get_my_flights_by_airline_company' for airline users
        #     airline_company = request.query_params['airline']
        #     flights = airlinefacade.get_flights_by_airline_company(request=request, airline_company_id=airline_company)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info('Get flights by airline company attempt')
        #     return Response(serializer.data)
        
        # elif 'departure' in request.query_params:
        #     # Handle 'get_my_flights_by_departure_time/date' for airline users
        #     departure_time = request.query_params['departure']
        #     flights = airlinefacade.get_flights_by_departure_date(request=request, departure_time=departure_time)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info('get flights by departure date/time attempt')
        #     return Response(serializer.data)           
        
        # elif 'landing' in request.query_params:
        #     # Handle 'get_my_flights_by_departure_time/date' for airline users
        #     landing_time = request.query_params['landing']
        #     flights = airlinefacade.get_flights_by_landing_date(request=request, landing_time=landing_time)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info('get flights by landing date/time attempt')
        #     return Response(serializer.data)
        
        # elif 'id' in request.query_params:
        #     # Handle 'get a specific flight' for other users
        #     id = request.query_params['id']
        #     flight = airlinefacade.get_flight_by_id(request=request, id=id)  
        #     serializer = DisplayFlightSerializer(flight)
        #     flight_logger.info('get flight by id attempt')
        #     return Response(serializer.data)

        # elif 'arrival' in request.query_params:
        #     # Handles the get arrival flights of a certain country for the next 12 hours
        #     arrival = request.query_params['arrival']
        #     flights = airlinefacade.get_arrival_flights_by_country_id(request=request, country_id=arrival)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info('get arrival flights by country id attempt')
        #     return Response(serializer.data)

        # elif 'depar_flights' in request.query_params:
        #     # Handles the get departure flights of a certain country for the next 12 hours  
        #     depar_flights = request.query_params['depar_flights']
        #     flights = airlinefacade.get_departure_flights_by_country_id(request=request, country_id=depar_flights)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info('get departure flights by country id attempt')
        #     return Response(serializer.data)
        
        # elif 'my' in request.query_params:

        #     if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
        #         return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        #     # my = request.query_params['my']
        #     id = request.user.airlinecompany.id
        #     flights = airlinefacade.get_my_flights(request=request, airline_company_id=id)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info(f"Attempted get my flights - airline {request.user.airlinecompany.id}")
        #     return Response(serializer.data)
            
        # else:
        #     # Handle 'get_all_flights' for other users
        #     flights = airlinefacade.get_all_flights(request=request)
        #     serializer = DisplayFlightSerializer(flights, many=True)
        #     flight_logger.info('get all flights attempt')
        #     return Response(serializer.data)
    
    
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
            return Response({"message": "Flight Created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
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
                return Response({"message": "Flight Updated successfully", "data": serializer.validated_data}, status=status.HTTP_201_CREATED)
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
        return Response(airlinefacade.remove_flight(request=request, flight_id=request.query_params['id'] ,airlinecompany=airlinecompany))








