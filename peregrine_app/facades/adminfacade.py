"""Admin facade, Most permissions are allowed,
 (other than a couple of actiosn permitted for a customer and an airline),
 it's structure and functionality is similar to the child facades(customer,airline ....)"""

""" The "transaction.atomic()" method makes sure that in case of encountering, a problem
of adding one of the 2 (or user_form , or customer_form) then it won't add anything to the DB
"""

# Importing facadebase to inherit from , and the required utilities
from .facadebase import FacadeBase
from django.db import transaction
from peregrine_app.exceptions import AccessDeniedError

class AdministratorFacade(FacadeBase):

    
    def __init__(self, user_group):
        super().__init__(dals=['customer_dal', 'airline_company_dal', 'administrator_dal','user_dal','group_dal','flight_dal','ticket_dal'])
        self._user_group = user_group
        if not self._user_group == 'admin':
            raise ValueError('Invalid user group')
        self.add_user_allowed = False    # allowing the add_user method work only when add_customer,add_admin , add_airline is requested

    @property
    def accessible_dals(self):
        return [('customer_dal', ['get_all_customers', 'add_customer' , 'remove_customer','get_customer_by_id']),
                ('airline_company_dal', ['add_airline_company', 'remove_airline_company', 'get_all_airline_companies']),
                ('administrator_dal', ['add_new_admin', 'remove_admin','get_all_admins', 'get_admin_by_id']),
                ('user_dal', ['remove_user','add_user']),
                ('flight_dal', ['get_flights_by_airline_company_id']),
                ('ticket_dal', ['get_tickets_by_customer_id']),
                ('group_dal', ['get_userRole_by_role','get_all_userRoles'])]


    def __enable_add_user(self):        # the __ before the name indicates that this is a prive function (which is still accessable from outside the class but "harder" to find)
        self.add_user_allowed = True
    
    def __disable_add_user(self):
        self.add_user_allowed = False


    def get_all_customers(self, request):
        if self.check_access('customer_dal', 'get_all_customers'):
            return self.customer_dal.get_all_customers()
        else:
            raise AccessDeniedError
                       
    def remove_customer(self, request, customer_id):
        if (self.check_access('user_dal', 'remove_user')) and (self.check_access('ticket_dal', 'get_tickets_by_customer_id')) and (self.check_access('customer_dal', 'get_customer_by_id')) :

            customer = self.customer_dal.get_customer_by_id(customer_id=customer_id)
            if customer is None:
                return ("Customer not found")
            user_id = customer.user_id.id
            tickets = self.ticket_dal.get_tickets_by_customer_id(customer_id=customer_id)
            if  tickets.exists():
                return ("This customer has an on going active ticket thus cannot be deleted")
            try:
                self.user_dal.remove_user(id=user_id)
                return ('Customer removed successfully')         
            except Exception as e:
                print(f"An error occurred while removing customer: {e}")
                return None
        else:
            raise AccessDeniedError


            
    def add_airline(self, request, user_data ,data):
        if (self.check_access('airline_company_dal', 'add_airline_company')) and (self.check_access('group_dal', 'get_userRole_by_role')) and (self.check_access('user_dal','add_user')) :
            self.__enable_add_user()  
            try:
                user_data['password'] = user_data['password1']
                group = self.group_dal.get_userRole_by_role(user_role='airline')
                with transaction.atomic(): 
                    new_user = self.user_dal.add_user(data=user_data)
                    if new_user is not None:
                        new_user.groups.add(group) 
                        data['user_id'] = new_user
                        self.airline_company_dal.add_airline_company(data=data)
            except Exception as e:
                transaction.set_rollback(True)
                print(f"An error occurred while adding airline: {e}")
                return None
            finally:    
                self.__disable_add_user()
        else:
            raise AccessDeniedError
          
    def remove_airline(self, request, id):
        if (self.check_access('user_dal', 'remove_user')) and (self.check_access('flight_dal', 'get_flights_by_airline_company_id')):

                airline = self.airline_company_dal.get_airline_company_by_id(id=id)
                if airline is None:
                        return ('Airline not found')
                user_id = airline.user_id.id
                flights = self.flight_dal.get_flights_by_airline_company_id(airline_company_id=id)
                if (flights.exists()):
                    return ("This airline has an active flights, thus cannot be removed")
                try:
                    self.user_dal.remove_user(id=user_id)
                    return ({'Flight removed successfully'})
                except Exception as e:
                    print(f"An error occurred while removing airline: {e}")
                    return None
        else:
            raise AccessDeniedError 


    def get_all_admins(self, request):
        if self.check_access('administrator_dal', 'get_all_admins'):        
            return self.administrator_dal.get_all_admins()  
        else:
            raise AccessDeniedError 

    def get_admin_by_id(self, request, admin_id):
        if self.check_access('administrator_dal', 'get_admin_by_id'):
            return self.administrator_dal.get_admin_by_id(id=admin_id)
        else:
            raise AccessDeniedError 

    def add_administrator(self, request, user_data, data):
        if self.check_access('administrator_dal', 'add_new_admin') and (self.check_access('user_dal','add_user')) and (self.check_access('group_dal', 'get_userRole_by_role')) :
            self.__enable_add_user()
            try:
                group = self.group_dal.get_userRole_by_role(user_role='admin')
                with transaction.atomic(): 
                    new_user = self.user_dal.add_user(data=user_data)
                    if new_user is not None:
                        new_user.groups.add(group)
                        new_user.is_staff = True # Set staff status to True
                        new_user.is_superuser = False # Set superuser status to True
                        new_user.save()                    
                        data['user_id'] = new_user
                        return self.administrator_dal.add_new_admin(data=data)
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                print(f"An error occurred while adding admin: {e}")
                return None               
            finally:
                 self.__disable_add_user()
        else:
            raise AccessDeniedError

    def remove_administrator(self, request, id):
        if self.check_access('user_dal', 'remove_user'):
            try:
                admin = self.administrator_dal.get_admin_by_id(id=id)
                user_id = admin.user_id.id
                return self.user_dal.remove_user(id=user_id)
            except Exception as e:
                print(f"An error occurred while removing admin: {e}")
                return None
        else:
            raise AccessDeniedError
        
