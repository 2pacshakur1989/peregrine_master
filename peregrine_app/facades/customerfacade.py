"""CustomerFacade is the customer's "app" or we can call it permissions.
It inherits the generic get functions from FacadeBase. Initializing its constructor,
requests the permitted dals from the Father class (Facadebase) """

# Importing the needed Facade and the needed utilities
from .facadebase import FacadeBase
from django.db import transaction
from peregrine_app.decorators import allowed_users 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from peregrine_app.loggers import customerfacade_logger
from peregrine_app.loggers import ticket_logger

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
        return [('customer_dal', ['update_customer','get_customer_by_id', 'get_customer_by_user_id']),('flight_dal', ['get_flight_by_id']) ,('ticket_dal', ['add_ticket', 'remove_ticket', 'get_ticket_by_id', 'get_tickets_by_customer_id']),('user_dal', ['update_user', 'get_user_by_id', 'get_user_by_username'])]
        

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))             
    def add_ticket(self, request, customer, flight_id):
        if (self.check_access('ticket_dal', 'add_ticket')) and (self.check_access('ticket_dal', 'get_tickets_by_customer_id')) and (self.check_access('flight_dal', 'get_flight_by_id')):
            try:
                tickets = self.ticket_dal.get_tickets_by_customer_id(customer_id=customer.id)
                for ticket in tickets:
                    if ticket.flight_id.id == int(flight_id):
                        # ticket_logger.info(f"Cannot add a ticket twice (it seems that this ticket is already added) - Customer : {request.user.customer}")
                        return None
                        # return ('Cannot add a ticket twice (it seems that this ticket is already added)')
                flight = self.flight_dal.get_flight_by_id(id=flight_id)
                if flight is None:
                    # ticket_logger.info('Flight not found')
                    return ('Flight not found')
                if flight.remaining_tickets == 0:
                    # ticket_logger.info('The selected flight has no available tickets. In case of canecllation please check later')
                    return ('The selected flight has no available tickets. In case of canecllation please check later')
                ticket_data = {
                        'flight_id': flight,
                        'customer_id': customer}
                self.ticket_dal.add_ticket(data=ticket_data) 
                flight.remaining_tickets = (flight.remaining_tickets) - 1
                flight.save()
                return ({'Ticket added successfully'})
            except Exception as e:
                customerfacade_logger.error(f"An error occurred while adding ticket: {e}")
                print(f"An error occurred while adding ticket: {e}")
                return None
        else:
            customerfacade_logger.error('Dal is not accessible')
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
                    transaction.set_rollback(True)
                    customerfacade_logger.error(f"An error occurred while removing ticket: {e}")
                    print(f"An error occurred while removing ticket: {e}")
                    return None
        else:
            customerfacade_logger.error('Dal is not accessible')
            raise AccessDeniedError


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))  
    def get_my_tickets(self, request, customer_id):
        if self.check_access('ticket_dal', 'get_tickets_by_customer_id'):
            try:
                return self.ticket_dal.get_tickets_by_customer_id(customer_id=customer_id)
            except Exception as e:
                customerfacade_logger.error(f"An error occurred while fetching tickets: {e}")
                print(f"An error occurred while fetching tickets: {e}")
                return None
        else:
            customerfacade_logger.error('Dal is not accessible')
            raise AccessDeniedError


    # @method_decorator(login_required)
    # @method_decorator(allowed_users(allowed_roles=['customer'])) 
    # def update_customer(self,request ,customer_id,user_id, user_data, data, currentpassword):
    #     if (self.check_access('customer_dal','update_customer')) and (self.check_access('user_dal','update_user')) :
    #         try:
    #             if (user_data['current_password'] is not None) and (user_data['password1'] is not None) and (user_data['password2'] is not None):
    #                 current_password_from_new_data = user_data['current_password']
    #                 match_password = check_password(current_password_from_new_data, currentpassword)
    #                 if not match_password:
    #                     customerfacade_logger.error("Incorrect current password")
    #                     print("Incorrect current password")
    #                     return None
    #                 else:
    #                     user_data['password'] = user_data['password1']
    #             with transaction.atomic():  
                    
    #                 update_user = self.user_dal.update_user(id=user_id,data=user_data)
    #                 update_customer = self.customer_dal.update_customer(customer_id=customer_id,data=data)
    #                 return update_user, update_customer
    #         except Exception as e:
    #             # rollback the update
    #             # transaction.set_rollback(True)
    #             customerfacade_logger.error(f"An error occurred while adding a customer: {e}")
    #             print(f"An error occurred while adding a customer: {e}")
    #             return None
    #     else:
    #         customerfacade_logger.error('Dal is not accessible')
    #         raise AccessDeniedError

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer'])) 
    def update_customer(self, request, customer_id, user_id, user_data, data, currentpassword):
        if (self.check_access('customer_dal','update_customer')) and (self.check_access('user_dal','update_user')):
            try:
                if 'current_password' in user_data or 'password1' in user_data or 'password2' in user_data:
                    current_password_from_new_data = user_data.get('current_password')
                    password1_from_new_data = user_data.get('password1')
                    password2_from_new_data = user_data.get('password2')
                    if current_password_from_new_data and password1_from_new_data and password2_from_new_data:
                        match_password = check_password(current_password_from_new_data, currentpassword)
                        if not match_password:
                            customerfacade_logger.error("Incorrect current password")
                            print("Incorrect current password")
                            return None
                        elif password1_from_new_data != password2_from_new_data:
                            customerfacade_logger.error("New passwords do not match")
                            print("New passwords do not match")
                            return None
                        else:
                            user_data['password'] = password1_from_new_data
                    else:
                        customerfacade_logger.error("All password fields must be filled")
                        print("All password fields must be filled")
                        return None

                with transaction.atomic():  
                    update_user = self.user_dal.update_user(id=user_id, data=user_data)
                    update_customer = self.customer_dal.update_customer(customer_id=customer_id, data=data)
                    return update_user, update_customer
            except Exception as e:
                # rollback the update
                # transaction.set_rollback(True)
                customerfacade_logger.error(f"An error occurred while updating a customer: {e}")
                print(f"An error occurred while updating a customer: {e}")
                return None
        else:
            customerfacade_logger.error('Dal is not accessible')
            raise AccessDeniedError

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def get_customer_by_id(self, request, customer_id, customer_instance):
        if self.check_access('customer_dal', 'get_customer_by_id'):
            try:
                if customer_instance.id == int(customer_id):
                    return self.customer_dal.get_customer_by_id(customer_id=customer_id)
            except Exception as e:
                customerfacade_logger.error(f"An error occurred while fetching customer: {e}")
                print(f"An error occurred while fetching customer: {e}")
                return None
        else:
            customerfacade_logger.error('Dal is not accessible')
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
                customerfacade_logger.error(f"An error occurred while fetching flight: {e}")
                print(f"An error occurred while fetching flight: {e}")
                return None
        else:
            customerfacade_logger.error('Dal is not accessible')
            raise AccessDeniedError 
        
    # @method_decorator(login_required)
    # @method_decorator(allowed_users(allowed_roles=['customer']))
    # def get_customer_by_username(self, request, username):
    #     if (self.check_access('customer_dal', 'get_customer_by_username')):
    #         try:
    #             customer = self.customer_dal.get_customer_by_username(username=username)
    #             if customer is None:
    #                 return None
    #             return customer
    #         except Exception as e:
    #             customerfacade_logger.error(f"An error occurred while fetching customer: {e}")
    #             print(f"An error occurred while fetching customer: {e}")
    #             return None
    #     else:
    #         customerfacade_logger.error('Dal is not accessible')
    #         raise AccessDeniedError 
        
    # @method_decorator(login_required)
    # @method_decorator(allowed_users(allowed_roles=['customer']))
    # def get_user_by_username(self,request, username):
    #     if (self.check_access('user_dal', 'get_user_by_username')):
    #         try:
    #             user = self.user_dal.get_user_by_username(username=username)
    #             if user is None:
    #                 return None
    #             return user
    #         except Exception as e:
    #             customerfacade_logger.error(f"An error occurred while fetching user: {e}")
    #             print(f"An error occurred while fetching user: {e}")
    #             return None
    #     else:
    #         customerfacade_logger.error('Dal is not accessible')
    #         raise AccessDeniedError  
    # 
    # 
    # 
    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def get_customer_by_user_id(self, request, id):
        if (self.check_access('customer_dal', 'get_customer_by_user_id')):
            try:
                customer = self.customer_dal.get_customer_by_user_id(id=id)
                if customer is None:
                    return None
                return customer
            except Exception as e:
                customerfacade_logger.error(f"An error occurred while fetching customer: {e}")
                print(f"An error occurred while fetching customer: {e}")
                return None
        else:
            customerfacade_logger.error('Dal is not accessible')
            raise AccessDeniedError 
        
    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def get_user_by_user_id(self,request, id):
        if (self.check_access('user_dal', 'get_user_by_id')):
            try:
                user = self.user_dal.get_user_by_id(id=id)
                if user is None:
                    return None
                return user
            except Exception as e:
                customerfacade_logger.error(f"An error occurred while fetching user: {e}")
                print(f"An error occurred while fetching user: {e}")
                return None
        else:
            customerfacade_logger.error('Dal is not accessible')
            raise AccessDeniedError               
    