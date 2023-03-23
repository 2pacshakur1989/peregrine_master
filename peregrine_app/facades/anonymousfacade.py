"""Anonymous facade is the login interface, it inherits the generic get functions
from FacadeBase, the permitted Dal/s, and has an Add cusomter method for signing up. 
It checks the type of user logged in, according to the group he's assigned to,
and returns the correct Facade """

# Importing the right facade and the required utilities
from .facadebase import FacadeBase
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.facades.airlinefacade import AirlineFacade
from peregrine_app.facades.customerfacade import CustomerFacade
from peregrine_app.exceptions import AccessDeniedError
from django.db import transaction


class AnonymousFacade(FacadeBase):

    def __init__(self):
        super().__init__(dals=['user_dal', 'customer_dal' ,'token_dal'])
        self.add_user_allowed = False    # allowing the add_user method work only when add_customer,add_admin , add_airline is requested

    @property
    def accessible_dals(self):
        return [('user_dal', ['add_user','get_user_by_username']),
                 ('customer_dal', ['add_customer']),
                 ('token_dal', ['create_token', 'delete_token', 'get_token_by_user']),
                 ('group_dal', ['get_userRole_by_role'])]
    
    def get_facade_for_user(self,user):
        user_groups = user.groups.all()
        for group in user_groups:
            if group.name == 'admin':
                return AdministratorFacade()
            elif group.name == 'airline':
                return AirlineFacade()
            elif group.name == 'customer':
                return CustomerFacade()
        return AnonymousFacade()
        
    def __enable_add_user(self):        # the __ before the name indicates that this is a prive function (which is still accessable from outside the class but "harder" to find)
        self.add_user_allowed = True
    
    def __disable_add_user(self):
        self.add_user_allowed = False

    def add_customer(self, user_data, data):
        if (self.check_access('customer_dal','add_customer')) and (self.check_access('user_dal','add_user')) and (self.check_access('group_dal', 'get_userRole_by_role')):
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
                    transaction.set_rollback(True)
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                print(f"An error occurred while adding a customer: {e}")
                return None
            finally:
                self.__disable_add_user()
        else:
            raise AccessDeniedError
