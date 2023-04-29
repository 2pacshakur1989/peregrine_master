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
from django.contrib.auth import authenticate, login, logout
from peregrine_app.loggers import anonymousfacade_logger
from rest_framework_simplejwt.tokens import AccessToken


class AnonymousFacade(FacadeBase):

    def __init__(self):
        super().__init__(dals=['user_dal', 'customer_dal' ,'token_dal'])
        # self.session = None
        self.add_user_allowed = False    # allowing the add_user method work only when add_customer,add_admin , add_airline is requested

    @property
    def accessible_dals(self):
        return [('user_dal', ['add_user','get_user_by_username']),
                 ('customer_dal', ['add_customer']),
                 ('token_dal', ['create_token', 'delete_token', 'get_token_by_user']),
                 ('group_dal', ['get_userRole_by_role'])]
    

        
    def __enable_add_user(self):        # the __ before the name indicates that this is a prive function (which is still accessable from outside the class but "harder" to find)
        self.add_user_allowed = True
    
    
    def __disable_add_user(self):
        self.add_user_allowed = False


    def add_customer(self, request, user_data, data):
        if (self.check_access('customer_dal','add_customer')) and (self.check_access('user_dal','add_user')) and (self.check_access('group_dal', 'get_userRole_by_role')):
            self.__enable_add_user()
            if (user_data is None) or (data is None):
                raise ValueError('no content')
            try:
                user_data['password'] = user_data['password1']
                group = self.group_dal.get_userRole_by_role(user_role='customer')
                with transaction.atomic():       
                    new_user = self.user_dal.add_user(data=user_data)
                    if new_user is not None:    
                        new_user.groups.add(group) 
                        data['user_id'] = new_user
                        new_customer = self.customer_dal.add_customer(data=data)
                        return new_customer
            except Exception as e:
                anonymousfacade_logger.error(f"An error occurred while adding a customer: {e}")
                print(f"An error occurred while adding a customer: {e}")
                return None
            finally:
                self.__disable_add_user()
        else:
            anonymousfacade_logger.error('Dal is not accessible')
            raise AccessDeniedError


    def login_func(self, request, **kwargs):

        print(request)
        username = kwargs.get('username')
        password = kwargs.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user=user)
            user_groups = user.groups.all()
            for group in user_groups:
                if group.name == 'admin':
                    facade = AdministratorFacade(user_group='admin')
                elif group.name == 'airline':
                    facade = AirlineFacade(user_group='airline')
                elif group.name == 'customer':
                    facade = CustomerFacade(user_group='customer')
                else:
                    facade = AnonymousFacade()

            token_payload = {
                'user_id': user.id,
                'username': user.username,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
            if user.groups.filter(name='airline').exists():
                token_payload['roles'] = ['airline']
            elif user.groups.filter(name='customer').exists():
                token_payload['roles'] = ['customer']
            elif user.groups.filter(name='admin').exists():
                token_payload['roles'] = ['admin']
            access_token = AccessToken.for_user(user)
            token = str(access_token)

            return {'access_token': token, 'payload': token_payload}
        else:
            anonymousfacade_logger.error('Invalid credentials')
            return ({'error': 'Invalid credentials'})
