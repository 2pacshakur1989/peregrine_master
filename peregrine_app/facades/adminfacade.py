from .facadebase import FacadeBase
from django.db import transaction
from peregrine_app.exceptions import AccessDeniedError, CannotRemoveAirline, CannotRemoveCustomer

# class AdministratorFacade:

#     def __init__(self):
#         self.facade_base = FacadeBase(['customer_dal', 'airline_company_dal', 'administrator_dal','user_dal','group_dal'])
#         self.accessible_dals = [('customer_dal', ['get_all_customers', 'add_customer' , 'remove_customer']),
#                                  ('airline_company_dal', ['add_airline_company', 'remove_airline_company']),
#                                  ('administrator_dal', ['add_new_admin', 'remove_admin']),
#                                  ('group_dal', ['get_userRole_by_role','get_all_userRoles'])]
#         self.add_user_allowed = False    # allowing the add_user method work only when add_customer,add_admin , add_airline is requested

#     def __getattr__(self, name):
#         for dal, funcs in self.accessible_dals:
#             if name in funcs:
#                 return getattr(getattr(self.facade_base, dal), name)
#         raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
#     def check_access(self, dal_name, method_name):
#         for dal in self.accessible_dals:
#             if dal[0] == dal_name and method_name in dal[1]:
#                 return True
#         return False
    
#     def __enable_add_user(self):        # the __ before the name indicates that this is a prive function (which is still accessable from outside the class but "harder" to find)
#         self.add_user_allowed = True
    
#     def __disable_add_user(self):
#         self.add_user_allowed = False

#     def get_all_customers(self):
#         if self.check_access('customer_dal', 'get_all_customers'):
#             try:
#                 return self.facade_base.customer_dal.get_all_customers()
#             except Exception as e:
#                 print(f"An error occurred while getting all customers: {e}")
#                 return None
#         else:
#             raise AccessDeniedError
        
#     def add_customer(self, user_data, data):
#         if self.check_access('customer_dal','add_customer'):
#             self.__enable_add_user()
#             try:
#                 group = self.facade_base.group_dal.get_userRole_by_role(user_role='customer')
#                 new_user = self.facade_base.user_dal.add_user(data=user_data)
#                 if new_user is not None:    
#                     new_user.groups.add(group) 
#                     data['user_id'] = new_user
#                     new_customer = self.facade_base.customer_dal.add_customer(data=data)
#                     return new_customer
#             except Exception as e:
#                 print(f"An error occurred while adding a customer: {e}")
#                 return None
#             finally:
#                 self.__disable_add_user()
#         else:
#             raise AccessDeniedError
        
#     def remove_customer(self, customer_id):
#         if self.check_access('customer_dal', 'remmove_customer'):
#             try:
#                 return self.facade_base.customer_dal.remove_customer(customer_id=customer_id)
#             except Exception as e:
#                 print(f"An error occurred while removing customer: {e}")
#                 return None
#         else:
#             raise AccessDeniedError
        
#     def add_airline(self, user_data ,data):
#         if self.check_access('airline_company_dal', 'add_airline_company'):
#             self.__enable_add_user()  
#             try:
#                 group = self.facade_base.group_dal.get_userRole_by_role(user_role='airline')
#                 new_user = self.facade_base.user_dal.add_user(data=user_data)
#                 if new_user is not None:
#                     new_user.groups.add(group) 
#                     data['user_id'] = new_user
#                     return self.facade_base.airline_company_dal.add_airline_company(data=data)
#             except Exception as e:
#                 print(f"An error occurred while adding airline: {e}")
#                 return None
#             finally:    
#                 self.__disable_add_user()
#         else:
#             raise AccessDeniedError
   
#     def remove_airline(self, id):
#         if self.check_access('airline_company_dal', 'remove_airline_company'):
#             try:
#                 return self.facade_base.airline_company_dal.remove_airline_company(id=id)
#             except Exception as e:
#                 print(f"An error occurred while removing airline: {e}")
#                 return None
#         else:
#             raise AccessDeniedError 

#     def add_administrator(self,user_data, data):
#         if self.check_access('administrator_dal', 'add_new_admin'):
#             self.__enable_add_user()
#             try:
#                 group = self.facade_base.group_dal.get_userRole_by_role(user_role='admin')
#                 new_user = self.facade_base.user_dal.add_user(data=user_data)
#                 if new_user is not None:
#                     new_user.groups.add(group)                    
#                     data['user_id'] = new_user
#                     return self.facade_base.administrator_dal.add_new_admin(data=data)
#             except Exception as e:
#                 print(f"An error occurred while adding admin: {e}")
#                 return None               
#             finally:
#                  self.__disable_add_user()
#         else:
#             raise AccessDeniedError
        
#     def remove_administrator(self, id):
#         if self.check_access('administrator_dal', 'remove_admin'):
#             try:
#                 return self.facade_base.administrator_dal.remove_admin(id=id)
#             except Exception as e:
#                 print(f"An error occurred while removing admin: {e}")
#                 return None
#         else:
#             raise AccessDeniedError






########## DO NOT CROSS UP ###########


class AdministratorFacade(FacadeBase):

    
    def __init__(self):
        super().__init__(dals=['customer_dal', 'airline_company_dal', 'administrator_dal','user_dal','group_dal','flight_dal','ticket_dal'])

        self.add_user_allowed = False    # allowing the add_user method work only when add_customer,add_admin , add_airline is requested

    @property
    def accessible_dals(self):
        return [('customer_dal', ['get_all_customers', 'add_customer' , 'remove_customer']),
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
            try:
                return self.customer_dal.get_all_customers()
            except Exception as e:
                print(f"An error occurred while getting all customers: {e}")
                return None
        else:
            raise AccessDeniedError
        
    def add_customer(self, user_data, data):
        if (self.check_access('customer_dal','add_customer')) and (self.check_access('user_dal','add_user')):
            self.__enable_add_user()
            try:
                group = self.group_dal.get_userRole_by_role(user_role='customer')
                with transaction.atomic(): 
                    new_user = self.user_dal.add_user(data=user_data)
                    if new_user is not None:    
                        new_user.groups.add(group) 
                        data['user_id'] = new_user
                        new_customer = self.customer_dal.add_customer(data=data)
                        return new_customer
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                print(f"An error occurred while adding a customer: {e}")
                return None
            finally:
                self.__disable_add_user()
        else:
            raise AccessDeniedError
               
    def remove_customer(self, customer_id):
        if (self.check_access('user_dal', 'remove_user')) and (self.check_access('ticket_dal', 'get_tickets_by_customer_id')) :
            try:  # No need for try/except
                tickets = self.ticket_dal.get_tickets_by_customer_id(customer_id=customer_id)
                if  tickets.exists():
                    raise CannotRemoveCustomer
                else:
                    customer = self.customer_dal.get_customer_by_id(customer_id=customer_id)
                    user_id = customer.user_id.id
                    return self.user_dal.remove_user(id=user_id)            
            except Exception as e:
                print(f"An error occurred while removing customer: {e}")
                return None
        else:
            raise AccessDeniedError


    def get_all_airlines(self):
        if self.check_access('airline_company_dal', 'get_all_airline_companies'):  
            try:
                return self.airline_company_dal.get_all_airline_companies()
            except Exception as e:
                print(f"An error occurred while fetching airline companies: {e}")
                return None
        else:
            raise AccessDeniedError                

    def add_airline(self, user_data ,data):
        if self.check_access('airline_company_dal', 'add_airline_company'):
            self.__enable_add_user()  
            try:
                group = self.group_dal.get_userRole_by_role(user_role='airline')
                with transaction.atomic(): 
                    new_user = self.user_dal.add_user(data=user_data)
                    if new_user is not None:
                        new_user.groups.add(group) 
                        data['user_id'] = new_user
                        return self.airline_company_dal.add_airline_company(data=data)
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                print(f"An error occurred while adding airline: {e}")
                return None
            finally:    
                self.__disable_add_user()
        else:
            raise AccessDeniedError
          
    def remove_airline(self, id):
        if (self.check_access('user_dal', 'remove_user')) and (self.check_access('flight_dal', 'get_flights_by_airline_company_id')):
            try:
                flights = self.flight_dal.get_flights_by_airline_company_id(airline_company_id=id)
                if flights == None:
                    airline = self.airline_company_dal.get_airline_company_by_id(id=id)
                    user_id = airline.user_id.id
                    return self.user_dal.remove_user(id=user_id)
                else:
                    raise CannotRemoveAirline
            except Exception as e:
                print(f"An error occurred while removing airline: {e}")
                return None
        else:
            raise AccessDeniedError 


    def get_all_admins(self):
        if self.check_access('administrator_dal', 'get_all_admins'):
            try:
                return self.administrator_dal.get_all_admins()  
            except Exception as e:
                print(f"An error occurred while fetching admins: {e}")
                return None
        else:
            raise AccessDeniedError 
              
    def add_administrator(self,user_data, data):
        if self.check_access('administrator_dal', 'add_new_admin'):
            self.__enable_add_user()
            try:
                group = self.group_dal.get_userRole_by_role(user_role='admin')
                with transaction.atomic(): 
                    new_user = self.user_dal.add_user(data=user_data)
                    if new_user is not None:
                        new_user.groups.add(group)
                        new_user.is_staff = True # Set staff status to True
                        new_user.is_superuser = True # Set superuser status to True
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