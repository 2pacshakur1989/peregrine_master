from rest_framework.decorators import api_view
from peregrine_app.peregrine_api.api_serializers.airline_serializer import AirlineSerializer, AddAirlineSerializer
from peregrine_app.peregrine_api.api_serializers.user_serializer import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.facades.customerfacade import CustomerFacade
from peregrine_app.facades.anonymousfacade import AnonymousFacade
from peregrine_app.facades.airlinefacade import AirlineFacade


airlinefacade = AirlineFacade()
adminfacade = AdministratorFacade()

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def airline(request, id=None):


    # GET REQUESTS
    if request.method == 'GET':

        if 'country_id' in request.query_params:
            # Handle 'get_airlines_by_country' for all users
            country_id = request.query_params['country_id']
            airlines = airlinefacade.get_airline_by_country(country_id=country_id)
            if (airlines is None) or (not airlines.exists()):
                return Response("No airlines found.", status=status.HTTP_404_NOT_FOUND)
            serializer = AirlineSerializer(airlines, many=True)
            return Response(serializer.data)
        
        elif 'id' in request.query_params:
            # Handle 'get_airlines_by_id' for all users
            id = request.query_params['id']
            airline = airlinefacade.get_airline_by_id(id=id)
            if airline is None:
                return Response("No airline found.", status=status.HTTP_404_NOT_FOUND)
            serializer = AirlineSerializer(airline)
            return Response(serializer.data)

        elif 'username' in request.query_params:  # For display the logged in airline 
            if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            airline_username = request.user.username
            username = request.query_params['username']
            if not username == airline_username:
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            airline = airlinefacade.get_airline_by_username(username=username)
            if airline is None:
                return Response("No airline found.", status=status.HTTP_404_NOT_FOUND)
            serializer = AirlineSerializer(airline)
            return Response(serializer.data)
       
        else:
            airlines = airlinefacade.get_all_airlines()
            if airlines is None:       
                return Response("No airlines found.", status=status.HTTP_404_NOT_FOUND)
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

        newairline = request.data # Extracting the raw data in order to extract the country id
        country_id = newairline.get('country_id')

        if user_serializer.is_valid():
        
            user_data = {
                'username': user_serializer.validated_data['username'],
                'email': user_serializer.validated_data['email'],
                'password': user_serializer.validated_data['password1']
            }
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if airline_serializer.is_valid():

            data = {
                'name': airline_serializer.validated_data['name'],
                'country_id': airline_serializer.validated_data['country_id']
            }
        else:
            return Response(airline_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if adminfacade.add_airline(user_data=user_data, data=data) == 5 :
            return Response("Invalid country ID", status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserSerializer(user_data)
        airline_serializer = AddAirlineSerializer(data)
        return Response({"message": "Airline Created successfully","user_data":user_serializer.data ,"airline_data": airline_serializer.data}, status=status.HTTP_201_CREATED) 


    # PATCH REQUESTS
    if request.method == 'PATCH':
        # Validating the User
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='airline').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if str(request.user.airlinecompany.id) != id:
            return Response("Airline is allowed to update its own details ONLY", status=status.HTTP_403_FORBIDDEN)  
        # Creating new serializer instances with the existing objects and partial=True (to allow the fields to be optional for update)
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        airline_serializer = AddAirlineSerializer(request.user.airlinecompany, data=request.data, partial=True)
        if user_serializer.is_valid():

            user_data = {
            }
        # Use validated data instead of request.data
            if 'username' in request.data:
                user_data.update({'username': user_serializer.validated_data['username']})
            if 'email' in request.data:
                user_data.update({'email': user_serializer.validated_data['email']})
            if 'password1' in request.data:
                user_data.update({'password': user_serializer.validated_data['password1']})  
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if airline_serializer.is_valid():

            data = {
            }
             # Use validated data instead of request.data
            if 'name' in request.data:
                data.update({'name': airline_serializer.validated_data['name']})
            if 'country_id' in request.data:
                data.update({'country_id': airline_serializer.validated_data['country_id']})
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
       
        updating = airlinefacade.update_airline(airline_company_id=id, user_id=request.user.id ,user_data=user_data, data=data)
        if updating == 4 :
            return Response("Airline does not exist", status=status.HTTP_400_BAD_REQUEST)
        ### Solve the issue of the "country doesn't exist" in patch request
        
        updated_user_serializer = UserSerializer(user_data)
        updated_airline_serializer = AddAirlineSerializer(data)

        return Response({"message": "Airline Updated successfully", "data": {"user": updated_user_serializer.data, "airline": updated_airline_serializer.data}}, status=status.HTTP_201_CREATED)


    # DELETE REQUESTS
    if request.method == 'DELETE':
         # Validating the User - this action is permitted for the admin only
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if adminfacade.remove_airline(id=id) == True:
            return Response("Airline removed succesfully",  status=status.HTTP_202_ACCEPTED)
        elif adminfacade.remove_airline(id=id) == False:
            return Response("This airline has an active flights, thus cannot be removed", status=status.HTTP_400_BAD_REQUEST)
        elif adminfacade.remove_airline(id=id) == 4:
            return Response("Airline does not exist", status=status.HTTP_400_BAD_REQUEST)
        
       
        
              