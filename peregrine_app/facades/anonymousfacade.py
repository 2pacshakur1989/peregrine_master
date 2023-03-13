from .facadebase import FacadeBase
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect ,render
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.facades.airlinefacade import AirlineFacade
from peregrine_app.facades.customerfacade import CustomerFacade
from peregrine_app.exceptions import AccessDeniedError
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework_simplejwt.authentication import JWTAuthentication


# class AnonymousFacade:

#     def __init__(self):
#         self.facade_base = FacadeBase(['user_dal', 'customer_dal'])
#         self.accessible_dals = [('user_dal', ['add_user'], ['get_user_by_username']), ('customer_dal', ['add_customer'])]
#         self.add_user_allowed = False
        
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
    
#     def get_facade_for_user(self,user):
#         user_groups = user.groups.all()
#         for group in user_groups:
#             if group.name == 'admin':
#                 return AdministratorFacade()
#             elif group.name == 'airline':
#                 return AirlineFacade()
#             elif group.name == 'customer':
#                 return CustomerFacade()
#         return AnonymousFacade()
    
#     def __enable_add_user(self):        # the __ before the name indicates that this is a prive function (which is still accessable from outside the class but "harder" to find)
#         self.add_user_allowed = True
    
#     def __disable_add_user(self):
#         self.add_user_allowed = False
    
#     def add_customer(self, user_data, data):
#         if self.check_access('customer_dal','add_customer'):
#             self.__enable_add_user()
#             try:
#                 group = self.facade_base.group_dal.get_userRole_by_role(user_role='customer')
#                 with transaction.atomic():  
#                     new_user = self.facade_base.user_dal.add_user(data=user_data)
#                     if new_user is not None:    
#                         new_user.groups.add(group) 
#                         data['user_id'] = new_user
#                         new_customer = self.facade_base.customer_dal.add_customer(data=data)
#                         return new_customer
#             except Exception as e:
#                 print(f"An error occurred while adding a customer: {e}")
#                 return None
#             finally:
#                 self.__disable_add_user()
#         else:
#             raise AccessDeniedError








########## DO NOT CROSS UP ###########



class AnonymousFacade(FacadeBase):

    def __init__(self):
        super().__init__(dals=['user_dal', 'customer_dal'])
        self.add_user_allowed = False

    @property
    def accessible_dals(self):
        return [('user_dal', ['add_user'], ['get_user_by_username']), ('customer_dal', ['add_customer'])]
    
    # def get_facade_for_user(self,user):
    #     user_groups = user.groups.all()
    #     for group in user_groups:
    #         if group.name == 'admin':
    #             return AdministratorFacade()
    #         elif group.name == 'airline':
    #             return AirlineFacade()
    #         elif group.name == 'customer':
    #             return CustomerFacade()
    #     return AnonymousFacade()
    
    def get_facade_for_user(self,user,token):
        user_groups = user.groups.all()
        # decoded_token = JWTAuthentication().get_validated_token(token)
        
        for group in user_groups:
            if (group.name == 'admin') and (token['roles'] == ['admin']):
                return AdministratorFacade()
            elif (group.name == 'airline') and (token['roles'] == ['airline']):
                return AirlineFacade()
            elif (group.name == 'customer') and (token['roles'] == ['customer']):
                return CustomerFacade()
        return AnonymousFacade()
    
    def __enable_add_user(self):        # the __ before the name indicates that this is a prive function (which is still accessable from outside the class but "harder" to find)
        self.add_user_allowed = True
    
    def __disable_add_user(self):
        self.add_user_allowed = False
    
    def add_customer(self, user_data, data):
        if self.check_access('customer_dal','add_customer'):
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
                print(f"An error occurred while adding a customer: {e}")
                return None
            finally:
                self.__disable_add_user()
        else:
            raise AccessDeniedError
