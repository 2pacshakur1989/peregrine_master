from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.facades.customerfacade import CustomerFacade
from peregrine_app.peregrine_api.api_serializers.ticket_serializer import TicketSerializer

customerfacade = CustomerFacade(user_group='customer')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def ticket(request, flight_id=None):

    # GET REQUESTS
    if request.method == 'GET':

        if 'id' in request.query_params:
            if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            # Handle 'get_airlines_by_country' for all users
            id = request.query_params['id']
            ticket = customerfacade.get_ticket_by_id(request=request, ticket_id=id)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)  

        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        customer_id = request.user.customer.id
        tickets = customerfacade.get_my_tickets(request=request, customer_id=customer_id)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


    # POST REQUESTS
    if request.method == 'POST':

        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if 'flight_id' in request.query_params:
            flight_id = request.query_params['flight_id'] 

        customer = request.user.customer
        serializer = TicketSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        new_ticket = customerfacade.add_ticket(request=request, customer=customer, flight_id=flight_id)
        return Response(new_ticket)
    

    # DELETE REQUESTS
    if request.method == 'DELETE':

        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if 'ticket_id' in request.query_params:
            ticket_id = request.query_params['ticket_id'] 
        return Response(customerfacade.remove_ticket(request=request, id=ticket_id))




