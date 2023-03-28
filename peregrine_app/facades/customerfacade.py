"""CustomerFacade is the customer's "app" or we can call it permissions.
It inherits the generic get functions from FacadeBase. Initializing its constructor,
requests the permitted dals from the Father class (Facadebase) """

# Importing the needed Facade and the needed utilities
from .facadebase import FacadeBase
from django.db import transaction
from peregrine_app.decorators import allowed_users 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

 # Custom made error, which handles the case, 
 # of a function requesting a DAL or a function which are not initialized in the constructor
from peregrine_app.exceptions import AccessDeniedError   


class CustomerFacade(FacadeBase):

    def __init__(self, user_group):
        super().__init__(dals=['customer_dal', 'ticket_dal', 'user_dal'])
        self._user_group = user_group
        if not self._user_group == 'customer':
            raise ValueError('Invalid user group')
           
    @property
    def accessible_dals(self):
        return [('customer_dal', ['update_customer','get_customer_by_id']),('flight_dal', ['get_flight_by_id']) ,('ticket_dal', ['add_ticket', 'remove_ticket', 'get_ticket_by_id', 'get_tickets_by_customer_id']),('user_dal', ['update_user', 'get_user_by_id'])]
        

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))             
    def add_ticket(self, request, customer, flight_id):
        if (self.check_access('ticket_dal', 'add_ticket')) and (self.check_access('ticket_dal', 'get_tickets_by_customer_id')) and (self.check_access('flight_dal', 'get_flight_by_id')):
            
            tickets = self.ticket_dal.get_tickets_by_customer_id(customer_id=customer.id)

            for ticket in tickets:
                if ticket.flight_id.id == int(flight_id):
                    return ('Cannot add a ticket twice (it seems that this ticket is already added)')
            flight = self.flight_dal.get_flight_by_id(id=flight_id)
            if flight is None:
                return ('Flight not found')
            if flight.remaining_tickets == 0:
                return ('The selected flight has no available tickets. In case of canecllation please check later')
            ticket_data = {
                    'flight_id': flight,
                    'customer_id': customer}
            self.ticket_dal.add_ticket(data=ticket_data) 
            flight.remaining_tickets = (flight.remaining_tickets) - 1
            flight.save()
            ticket = self.ticket_dal.get_tickets_by_flight_id(flight_id=flight_id)
            return ({'Ticket added successfully'})
        else:
            raise AccessDeniedError


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))  
    def remove_ticket(self, request, id):
        if (self.check_access('ticket_dal', 'remove_ticket')) and (self.check_access('ticket_dal', 'get_ticket_by_id')):        
            with transaction.atomic():
                try:
                    ticket = self.ticket_dal.get_ticket_by_id(id=id)
                    if ticket is None:
                        return ('Ticket not found')
                    flight = ticket.flight_id
                    flight.remaining_tickets = (flight.remaining_tickets) + 1
                    flight.save()
                    self.ticket_dal.remove_ticket(id=id)
                    return ('Ticket removed successfully')
                except Exception as e:
                    with transaction.atomic():
                        print(f"An error occurred while removing ticket: {e}")
                        return None
        else:
            raise AccessDeniedError


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))  
    def get_my_tickets(self, request, customer_id):
        if self.check_access('ticket_dal', 'get_tickets_by_customer_id'):
            try:
                return self.ticket_dal.get_tickets_by_customer_id(customer_id=customer_id)
            except Exception as e:
                print(f"An error occurred while fetching tickets: {e}")
                return None
        else:
            raise AccessDeniedError


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer'])) 
    def update_customer(self,request ,customer_id,user_id, user_data, data):
        if (self.check_access('customer_dal','update_customer')) and (self.check_access('user_dal','update_user')) :
            try:
                with transaction.atomic():  
                    update_user = self.user_dal.update_user(id=user_id,data=user_data)
                    update_customer = self.customer_dal.update_customer(customer_id=customer_id,data=data)
                    return update_user, update_customer
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                print(f"An error occurred while adding a customer: {e}")
                return None
        else:
            raise AccessDeniedError


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def get_customer_by_id(self, request, customer_id, customer_instance):
        if self.check_access('customer_dal', 'get_customer_by_id'):
            try:
                if customer_instance.id == int(customer_id):
                    return self.customer_dal.get_customer_by_id(customer_id=customer_id)
            except Exception as e:
                print(f"An error occurred while fetching customer: {e}")
                return None
        else:
            raise AccessDeniedError 


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def get_ticket_by_id(self, request, ticket_id, customer):
        if self.check_access('ticket_dal', 'get_ticket_by_id'):
            try:
                ticket = self.ticket_dal.get_ticket_by_id(id=ticket_id)
                if ticket is None:
                    return None
                if customer != ticket.customer_id:
                    return ('Not authorized')
                return ticket
            except Exception as e:
                print(f"An error occurred while fetching flight: {e}")
                return None
        else:
            raise AccessDeniedError 

    