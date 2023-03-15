from rest_framework.response import Response
from rest_framework.decorators import api_view
from peregrine_app.serializers import FlightSerializer
from django.http import JsonResponse
from peregrine_app.models import Flight
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from peregrine_app.facades.anonymousfacade import AnonymousFacade
from peregrine_app.facades.airlinefacade import AirlineFacade

anonymousfacade = AnonymousFacade()
airlinefacade = AirlineFacade()



# from rest_framework.permissions import BasePermission

# class IsAirline(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='airline').exists()

# @api_view(['GET', 'POST'])
# def flight_list(request):

#     if request.method == 'GET':
#         flights = Flight.objects.all()
#         serializer = FlightSerializer(flights, many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     if request.method == 'POST':
#         serializer = FlightSerializer(data=request.data)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print(serializer.errors)



# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# # @permission_classes([IsAirline])
# def flight_list(request):
#     if request.method == 'GET':
#         if request.user.groups.filter(name='airline').exists():
#             # Handle 'get_my_flights' for airline users
#             flights = airlinefacade.get_my_flights(airline_company_id=request.user)
#             serializer = FlightSerializer(flights, many=True)
#             return Response(serializer.data)
#         else:
#             # Handle 'get_all_flights' for other users
#             flights = anonymousfacade.get_all_flights()
#             serializer = FlightSerializer(flights, many=True)
#             return Response(serializer.data)
#     elif request.method == 'POST':
#         # Handle POST request to create a new flight
#         pass
#     elif request.method == 'PUT':
#         # Handle PUT request to update an existing flight
#         pass
#     elif request.method == 'DELETE':
#         # Handle DELETE request to delete an existing flight
#         pass

# @api_view(['GET', 'POST'])
# def flight_list(request):

#     if request.method == 'GET':
#         flights = anonymousfacade.get_all_flights()
#         serializer = FlightSerializer(flights, many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     if request.method == 'POST':
#         serializer = FlightSerializer(data=request.data)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print(serializer.errors)

# @api_view(['GET'])
# @permission_classes([IsAirline])
# def my_flight_list(request):
#     # Handle 'get_my_flights' for airline users only
#     flights = airlinefacade.get_my_flights(airline_company_id=request.user)
#     serializer = FlightSerializer(flights, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def flight_list(request):
#     if request.user.is_authenticated:
#         if request.user.groups.filter(name='airline').exists():
#             # Handle 'get_my_flights' for airline users
#             print(type(request.user.airlinecompany))
            
#             flights = airlinefacade.get_my_flights(airline_company_id=request.user.airlinecompany)
#             # print(flights)
#             serializer = FlightSerializer(flights, many=True)
#             return Response(serializer.data)
#         else:
#             # Handle 'get_all_flights' for other logged in users
#             flights = anonymousfacade.get_all_flights()
#             serializer = FlightSerializer(flights, many=True)
#             return Response(serializer.data)
#     else:
#         # Handle 'get_all_flights' for anonymous users
#         flights = anonymousfacade.get_all_flights()
#         serializer = FlightSerializer(flights, many=True)
#         return Response(serializer.data)




# @api_view(['GET'])
# def flight_list(request):
#     if request.user.is_authenticated:
#         if request.user.groups.filter(name='airline').exists():
#             # Handle 'get_my_flights' for airline users
#             print(type(request.user.airlinecompany))
            
#             flights = airlinefacade.get_my_flights(airline_company_id=request.user.airlinecompany)
#             # print(flights)
#             serializer = FlightSerializer(flights, many=True)
#             return Response(serializer.data)
#         else:
#             # Handle 'get_all_flights' for other logged in users
#             flights = anonymousfacade.get_all_flights()
#             serializer = FlightSerializer(flights, many=True)
#             return Response(serializer.data)
#     else:
#         # Handle 'get_all_flights' for anonymous users
#         flights = anonymousfacade.get_all_flights()
#         serializer = FlightSerializer(flights, many=True)
#         return Response(serializer.data)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def flight_list(request, id):



    # GET REQUESTS
    if request.method == 'GET':
        if 'origin' in request.query_params:
            # Handle 'get_flights_by_origin_country' for all users
            origin_country = request.query_params['origin']
            flights = anonymousfacade.get_flights_by_origin_country_id(origin_country_id=origin_country)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'destination' in request.query_params:
            # Handle 'get_flights_by_destination_country' for all users
            destination_country = request.query_params['destination']
            flights = anonymousfacade.get_flights_by_destination_country_id(destination_country_id=destination_country)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'airline' in request.query_params:
            # Handle 'get_my_flights_by_airline_company' for airline users
            airline_company = request.query_params['airline']
            flights = anonymousfacade.get_flights_by_airline_company(airline_company_id=airline_company)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        
        elif 'departure' in request.query_params:
            # Handle 'get_my_flights_by_departure_time/date' for airline users
            departure_time = request.query_params['departure']
            flights = anonymousfacade.get_flights_by_departure_date(departure_time=departure_time)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)           
        
        elif 'landing' in request.query_params:
            # Handle 'get_my_flights_by_departure_time/date' for airline users
            landing_time = request.query_params['landing']
            flights = anonymousfacade.get_flights_by_landing_date(landing_time=landing_time)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)           
        else:
            # Handle 'get_all_flights' for other users
            flights = anonymousfacade.get_all_flights()
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
    
    
    
    #POST REQUESTS
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.groups.filter(name='airline').exists():
                airlinecompany = request.user.airlinecompany
                serializer = FlightSerializer(data=request.data)
                if serializer.is_valid():
                    # Use validated data instead of request.data
                    new_flight = airlinefacade.add_flight(data=serializer.validated_data, airlinecompany=airlinecompany)
                    if new_flight == False:
                        return Response("Airline is allowed to add flights with its Id ONLY", status=status.HTTP_403_FORBIDDEN)
                    serializer = FlightSerializer(new_flight)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Only airline users can add flights.", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)



    # PUT REQUESTS
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            if request.user.groups.filter(name='airline').exists():
                airlinecompany = request.user.airlinecompany
                serializer = FlightSerializer(data=request.data)
                if serializer.is_valid():
                    update_flight = airlinefacade.update_flight(data=serializer.validated_data,flight_id=id, airlinecompany=airlinecompany)
                    if update_flight == False:
                        return Response("Airline is allowed to update flights with its Id ONLY", status=status.HTTP_403_FORBIDDEN)
                    elif update_flight == 1 :
                        return Response("Flight Does Not Exist", status=status.HTTP_403_FORBIDDEN)
                    elif update_flight == 2:
                        return Response("Flight id Does Not Exist", status=status.HTTP_403_FORBIDDEN)
                    serializer = FlightSerializer(update_flight)
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Only airline users can update flights.", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)


    
    # # DELETE REQUESTS
    # elif request.method == 'DELETE':
    #     if not request.user.is_authenticated:
    #         if request.user.groups.filter(name='airline').exists():
    #             airlinecompany = request.user.airlinecompany
    #             serializer = FlightSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 remove_flight = airlinefacade.remove_flight(flight_id=id)
    #                 if remove_flight == 0:
    #                     return Response("Cannot Remove Another Airline's Flight !", status=status.HTTP_403_FORBIDDEN)
    #                 elif remove_flight ==1:
    #                     return Response("This flight has an on going active/pruchased tickets thus cannot be removed !", status=status.HTTP_403_FORBIDDEN)
    #                 elif remove_flight == 2:
    #                     return Response("Flight id does not exist ", status=status.HTTP_204_NO_CONTENT)
    #                 return Response("Flight removed succesfully", serializer.data, status=status.HTTP_202_ACCEPTED)
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             return Response("Only airline users can update flights.", status=status.HTTP_403_FORBIDDEN)
    #     else:
    #         return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)





    # DELETE REQUESTS
    elif request.method == 'DELETE':
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())) :
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        airlinecompany = request.user.airlinecompany
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            remove_flight = airlinefacade.remove_flight(flight_id=id)
            if remove_flight == 0:
                return Response("Cannot Remove Another Airline's Flight !", status=status.HTTP_403_FORBIDDEN)
            elif remove_flight ==1:
                return Response("This flight has an on going active/pruchased tickets thus cannot be removed !", status=status.HTTP_403_FORBIDDEN)
            elif remove_flight == 2:
                return Response("Flight id does not exist ", status=status.HTTP_204_NO_CONTENT)
            return Response("Flight removed succesfully", serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




        


