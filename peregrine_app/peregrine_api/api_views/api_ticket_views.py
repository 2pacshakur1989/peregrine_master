from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.facades.customerfacade import CustomerFacade
from peregrine_app.peregrine_api.api_serializers.ticket_serializer import TicketSerializer
from peregrine_app.loggers import ticket_logger

customerfacade = CustomerFacade(user_group='customer')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def ticket(request):

    # GET REQUESTS
    if request.method == 'GET':


        if ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):

            customer = request.user.customer
            
            if 'id' in request.query_params:
                
                id = request.query_params['id']
                ticket = customerfacade.get_ticket_by_id(request=request, ticket_id=id ,customer=customer)
                serializer = TicketSerializer(ticket)
                ticket_logger.info(f"Attempted get ticket by id - customer {request.user.customer.id}")
                return Response(serializer.data)  
            
            customer_id = customer.id
            tickets = customerfacade.get_my_tickets(request=request, customer_id=customer_id)
            serializer = TicketSerializer(tickets, many=True)
            ticket_logger.info(f"Attempted get my tickets - customer {request.user.customer.id}")
            return Response(serializer.data)

        return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)


    # POST REQUESTS
    if request.method == 'POST':

        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)

        customer = request.user.customer
        serializer = TicketSerializer(data=request.data)
        if not serializer.is_valid():
            ticket_logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        new_ticket = customerfacade.add_ticket(request=request, customer=customer, flight_id=request.data['flight_id'])
        ticket_logger.info(f"Adding ticket attempt - customer {request.user.customer}")
        return Response(new_ticket)
    

    # DELETE REQUESTS
    if request.method == 'DELETE':

        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if 'id' in request.query_params:
            ticket_logger.info(f"Removing ticket attempt - customer {request.user.customer}")
            return Response(customerfacade.remove_ticket(request=request, id=request.query_params['id']))
        ticket_logger.info(f'Ticket id must be provided - customer {request.user.customer}')
        return Response("Ticket id must be provided.", status=status.HTTP_400_BAD_REQUEST)




