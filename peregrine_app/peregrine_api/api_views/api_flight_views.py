"""This is the Flight API view, it has different GET options which are all available to the anonymous user.
The POST, PUT,DELETE methods are permitted for the Airline companies ONLY! """

from rest_framework.decorators import api_view
from peregrine_app.peregrine_api.api_serializers.flight_serializer import FlightSerializer, DisplayFlightSerializer
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.facades.airlinefacade import AirlineFacade

airlinefacade = AirlineFacade(user_group='airline')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def flight(request, id=None):


    # GET REQUESTS
    if request.method == 'GET':

            
        if 'origin' in request.query_params:
            # Handle 'get_flights_by_origin_country' for all users
            origin_country = request.query_params['origin']
            flights = airlinefacade.get_flights_by_origin_country_id(origin_country_id=origin_country)
            serializer = DisplayFlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'destination' in request.query_params:
            # Handle 'get_flights_by_destination_country' for all users
            destination_country = request.query_params['destination']
            flights = airlinefacade.get_flights_by_destination_country_id(destination_country_id=destination_country)
            serializer = DisplayFlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'airline' in request.query_params:
            # Handle 'get_my_flights_by_airline_company' for airline users
            airline_company = request.query_params['airline']
            flights = airlinefacade.get_flights_by_airline_company(airline_company_id=airline_company)
            serializer = DisplayFlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'departure' in request.query_params:
            # Handle 'get_my_flights_by_departure_time/date' for airline users
            departure_time = request.query_params['departure']
            flights = airlinefacade.get_flights_by_departure_date(departure_time=departure_time)
            serializer = DisplayFlightSerializer(flights, many=True)
            return Response(serializer.data)           
        
        elif 'landing' in request.query_params:
            # Handle 'get_my_flights_by_departure_time/date' for airline users
            landing_time = request.query_params['landing']
            flights = airlinefacade.get_flights_by_landing_date(landing_time=landing_time)
            serializer = DisplayFlightSerializer(flights, many=True)
            return Response(serializer.data) 
        
        elif 'id' in request.query_params:
            # Handle 'get a specific flight' for other users
            id = request.query_params['id']
            flight = airlinefacade.get_flight_by_id(id=id)  
            serializer = DisplayFlightSerializer(flight)
            return Response(serializer.data)  
         
        else:
            # Handle 'get_all_flights' for other users
            flights = airlinefacade.get_all_flights()
            serializer = DisplayFlightSerializer(flights, many=True)
            return Response(serializer.data)
    
    
    #POST REQUESTS
    elif request.method == 'POST':
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        airlinecompany = request.user.airlinecompany
        serializer = FlightSerializer(data=request.data)       
        if serializer.is_valid():
            # Use validated data instead of request.data
            new_flight = airlinefacade.add_flight(data=serializer.validated_data, airlinecompany=airlinecompany)
            serializer = FlightSerializer(new_flight)
            return Response({"message": "Flight Created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # PUT REQUESTS
    elif request.method == 'PUT':
        if not ((request.user.is_authenticated) or (request.user.groups.filter(name='airline').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)                
        airlinecompany = request.user.airlinecompany
        serializer = FlightSerializer(data=request.data)     
        if serializer.is_valid():
            # Use validated data instead of request.data
            airlinefacade.update_flight(data=serializer.validated_data, flight_id=id, airlinecompany=airlinecompany)
            return Response({"message": "Flight Updated successfully", "data": serializer.validated_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DELETE REQUESTS
    elif request.method == 'DELETE':
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())) :
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        airlinecompany = request.user.airlinecompany  
        return Response(airlinefacade.remove_flight(flight_id=id,airlinecompany=airlinecompany))








