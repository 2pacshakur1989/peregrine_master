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

    
    def __init__(self):
        super().__init__(dals=['customer_dal', 'airline_company_dal', 'administrator_dal','user_dal','group_dal','flight_dal','ticket_dal'])

        self.add_user_allowed = False    # allowing the add_user method work only when add_customer,add_admin , add_airline is requested

    @property
    def accessible_dals(self):
        return [('customer_dal', ['get_all_customers', 'add_customer' , 'remove_customer','get_customer_by_id']),
                ('airline_company_dal', ['add_airline_company', 'remove_airline_company', 'get_all_airline_companies']),
                ('administrator_dal', ['add_new_admin', 'remove_admin','get_all_admins']),
                ('user_dal', ['remove_user','add_user']),
                ('flight_dal', ['get_flights_by_airline_company_id']),
                ('ticket_dal', ['get_tickets_by_customer_id']),
                ('group_dal', ['get_userRole_by_role','get_all_userRoles'])]


    def __enable_add_user(self):        # the __ before the name indicates that this is a prive function (which is still accessable from outside the class but "harder" to find)
        self.add_user_allowed = True
    
    def __disable_add_user(self):
        self.add_user_allowed = False


    def get_all_customers(self):
        if self.check_access('customer_dal', 'get_all_customers'):
                return self.customer_dal.get_all_customers()
        else:
            raise AccessDeniedError
        
    # def add_customer(self, user_data, data):
    #     if (self.check_access('customer_dal','add_customer')) and (self.check_access('user_dal','add_user')) and (self.check_access('group_dal', 'get_userRole_by_role')):
    #         self.__enable_add_user()
    #         try:
    #             group = self.group_dal.get_userRole_by_role(user_role='customer')
    #             with transaction.atomic():       
    #                 new_user = self.user_dal.add_user(data=user_data)
    #                 if new_user is not None:    
    #                     new_user.groups.add(group) 
    #                     data['user_id'] = new_user
    #                     new_customer = self.customer_dal.add_customer(data=data)
    #                     return new_customer
    #                 transaction.set_rollback(True)
    #         except Exception as e:
    #             # rollback the update
    #             transaction.set_rollback(True)
    #             print(f"An error occurred while adding a customer: {e}")
    #             return None
    #         finally:
    #             self.__disable_add_user()
    #     else:
    #         raise AccessDeniedError
               
    def remove_customer(self, customer_id):
        if (self.check_access('user_dal', 'remove_user')) and (self.check_access('ticket_dal', 'get_tickets_by_customer_id')) and (self.check_access('customer_dal', 'get_customer_by_id')) :

            customer = self.customer_dal.get_customer_by_id(customer_id=customer_id)
            if customer is None :
                return 4
            user_id = customer.user_id.id
            tickets = self.ticket_dal.get_tickets_by_customer_id(customer_id=customer_id)
            if  tickets.exists():
                return 3
            try:
                self.user_dal.remove_user(id=user_id)
                return True         
            except Exception as e:
                print(f"An error occurred while removing customer: {e}")
                return None
        else:
            raise AccessDeniedError


    def get_all_airlines(self):
        if self.check_access('airline_company_dal', 'get_all_airline_companies'):  
                return self.airline_company_dal.get_all_airline_companies()
        else:
            raise AccessDeniedError                

    def add_airline(self, user_data ,data):
        if (self.check_access('airline_company_dal', 'add_airline_company')) and (self.check_access('group_dal', 'get_userRole_by_role')) and (self.check_access('user_dal','add_user')) and (self.check_access('country_dal','get_country_by_id')):
            self.__enable_add_user()  
            try:
                country_id = data['country_id']
                country_id = country_id.id
                if self.country_dal.get_country_by_id(country_id=country_id) is None:
                    return 5
                group = self.group_dal.get_userRole_by_role(user_role='airline')
                with transaction.atomic(): 
                    new_user = self.user_dal.add_user(data=user_data)
                    if new_user is not None:
                        new_user.groups.add(group) 
                        data['user_id'] = new_user
                        return self.airline_company_dal.add_airline_company(data=data)
                    transaction.set_rollback(True)
            except Exception as e:
                print(f"An error occurred while adding airline: {e}")
                return None
            finally:    
                self.__disable_add_user()
        else:
            raise AccessDeniedError
          
    def remove_airline(self, id):
        if (self.check_access('user_dal', 'remove_user')) and (self.check_access('flight_dal', 'get_flights_by_airline_company_id')):

                airline = self.airline_company_dal.get_airline_company_by_id(id=id)
                if airline is None:
                        return 4
                user_id = airline.user_id.id
                flights = self.flight_dal.get_flights_by_airline_company_id(airline_company_id=id)
                if (flights.exists()):
                    return False
                try:
                    self.user_dal.remove_user(id=user_id)
                    return True
                except Exception as e:
                    print(f"An error occurred while removing airline: {e}")
                    return None
        else:
            raise AccessDeniedError 


    def get_all_admins(self):
        if self.check_access('administrator_dal', 'get_all_admins'):        
            return self.administrator_dal.get_all_admins()  
        else:
            raise AccessDeniedError 
              
    def add_administrator(self,user_data, data):
        if self.check_access('administrator_dal', 'add_new_admin')  and (self.check_access('group_dal', 'get_userRole_by_role')) :
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
                    transaction.set_rollback(True)
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                print(f"An error occurred while adding admin: {e}")
                return None               
            finally:
                 self.__disable_add_user()
        else:
            raise AccessDeniedError
        
    def remove_administrator(self, id):
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
        
