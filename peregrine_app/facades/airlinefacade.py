"""airlineFacade is the airline's "app" or we can call it permissions.
It inherits the generic get functions from FacadeBase. Initializing its constructor,
requests the permitted dals from the Father class (Facadebase) """

# Importing the right facade and the required utilities
from .facadebase import FacadeBase
from peregrine_app.exceptions import AccessDeniedError
from django.db import transaction
from peregrine_app.decorators import allowed_users 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from peregrine_app.loggers import airlinefacade_logger
from django.http import JsonResponse


class AirlineFacade(FacadeBase):
    
    def __init__(self, user_group):
        super().__init__(dals=['airline_company_dal', 'flight_dal','user_dal','ticket_dal', 'country_dal'])
        self._user_group = user_group
        if not self._user_group == 'airline':
            raise ValueError('Invalid user group')
        
    @property
    def accessible_dals(self):
        return [('airline_company_dal', ['update_airline_company', 'get_airline_company_by_id', 'get_airline_by_username','get_airline_by_user_id']), ('flight_dal', ['get_flights_by_airline_company_id','add_flight','update_flight', 'remove_flight','get_flight_by_id']),('user_dal', ['update_user', 'get_user_by_user_id']),('ticket_dal', ['get_tickets_by_flight_id']), ('country_dal', ['get_country_by_id'])]

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['airline'])) 
    def get_my_flights(self, request, airline_company_id):
        if self.check_access('flight_dal', 'get_flights_by_airline_company_id'):
            try:
                return self.flight_dal.get_flights_by_airline_company_id(airline_company_id=airline_company_id)
                    
            except Exception as e:
                airlinefacade_logger.error(f"An error occurred while fetching flights: {e}")
                print(f"An error occurred while fetching flights: {e}")
                return None
        airlinefacade_logger.error('Dal is not accessible')
        raise AccessDeniedError 


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['airline'])) 
    def update_airline(self, request, airline_company_id ,user_id, user_data, data, currentpassword):
        if (self.check_access('airline_company_dal','update_airline_company')) and (self.check_access('user_dal','update_user')) and (self.check_access('airline_company_dal','get_airline_company_by_id')) and (self.check_access('country_dal','get_country_by_id')):
            country_id = data['country_id']
            data['country_id'] = country_id.id
            try:
                if 'current_password' in user_data or 'password1' in user_data or 'password2' in user_data:
                    current_password_from_new_data = user_data.get('current_password')
                    password1_from_new_data = user_data.get('password1')
                    password2_from_new_data = user_data.get('password2')
                    if current_password_from_new_data and password1_from_new_data and password2_from_new_data:
                        match_password = check_password(current_password_from_new_data, currentpassword)
                        if not match_password:
                            airlinefacade_logger.error("Incorrect current password")
                            print("Incorrect current password")
                            return None
                        elif password1_from_new_data != password2_from_new_data:
                            airlinefacade_logger.error("New passwords do not match")
                            print("New passwords do not match")
                            return None
                        else:
                            user_data['password'] = password1_from_new_data
                    else:
                        airlinefacade_logger.error("All password fields must be filled")
                        print("All password fields must be filled")
                        return None     
                with transaction.atomic():  
                    update_user = self.user_dal.update_user(id=user_id,data=user_data)
                    update_airline = self.airline_company_dal.update_airline_company(id=airline_company_id,data=data)
                    return update_user, update_airline
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                airlinefacade_logger.error(f"facade : An error occurred while updating airline: {e}")
                print(f"facade : An error occurred while updating airline: {e}")
                return None
        airlinefacade_logger.error('Dal is not accessible')    
        raise AccessDeniedError
    

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['airline']))                
    def add_flight(self, request, data, airlinecompany):     # This is for the API
        if self.check_access('flight_dal', 'add_flight'):    
            try:
                data['airline_company_id'] = airlinecompany
                return self.flight_dal.add_flight(data=data)
            except Exception as e:
                airlinefacade_logger.error(f"An error occurred while adding flight: {e}")
                print(f"An error occurred while adding flight: {e}")
                return None
        airlinefacade_logger.error('Dal is not accessible')
        raise AccessDeniedError


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['airline'])) 
    def update_flight(self, request, flight_id, data ,airlinecompany):  # This is for API
        if (self.check_access('flight_dal', 'update_flight')) and (self.check_access('flight_dal', 'get_flight_by_id')):
            try:
                data['airline_company_id'] = airlinecompany.id

                origin = data['origin_country_id']
                data['origin_country_id'] = origin.id

                destination = data['destination_country_id']
                data['destination_country_id'] = destination.id
                
                flight = self.flight_dal.get_flight_by_id(id=flight_id)
                if flight is None:
                    return None
                if flight.airline_company_id != airlinecompany:
                    return None
                print(data['airline_company_id'])
                return self.flight_dal.update_flight(flight_id=flight_id,data=data)
            except Exception as e:
                airlinefacade_logger.error(f"An error occurred while updating flight: {e}")
                print(f"An error occurred while updating flight: {e}")
                return None
        airlinefacade_logger.error('Dal is not accessible')
        raise AccessDeniedError


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['airline'])) 
    def remove_flight(self, request, flight_id, airlinecompany):  # This is for the Api
        if (self.check_access('flight_dal', 'remove_flight')) and (self.check_access('ticket_dal', 'get_tickets_by_flight_id')) and (self.check_access('flight_dal', 'get_flight_by_id')) :   
            try:
                flight = self.flight_dal.get_flight_by_id(id=flight_id)
                if flight is None:
                    print('Flight does not exist')
                    return False
                if flight.airline_company_id.id != airlinecompany.id:
                    print('you are not authorized')
                    return False   # returning a cue value  (Cannot Remove Another Airline's Flight !)        
                tickets = self.ticket_dal.get_tickets_by_flight_id(flight_id=flight_id)
                if not tickets.exists():
                    return self.flight_dal.remove_flight(flight_id=flight_id)
                # return JsonResponse("This")
                print ({'This flight has an on going active/pruchased tickets thus cannot be removed'})
                return False # returning a cue value  (This flight has an on going active/pruchased tickets thus cannot be removed !)
            except Exception as e:
                airlinefacade_logger.error(f"An error occurred while removing flight: {e}")
                print(f"An error occurred while removing flight: {e}")
                return None
        airlinefacade_logger.error('Dal is not accessible')
        raise AccessDeniedError


    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['airline']))                   
    def get_airline_by_user_id(self, request, user_id, airline_user_id):
        if self.check_access('airline_company_dal', 'get_airline_by_user_id'):
            try:
                if str(airline_user_id) != user_id:
                    return None
                return self.airline_company_dal.get_airline_by_user_id(id=user_id)
            except Exception as e:
                airlinefacade_logger.error(f"An error occurred while fetching airline: {e}")
                print(f"An error occurred while fetching airline: {e}")
                return None
        airlinefacade_logger.error('Dal is not accessible')
        raise AccessDeniedError
    

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['airline']))                   
    def get_airline_by_username(self, request, username, airline_username):
        if self.check_access('airline_company_dal', 'get_airline_by_user_id'):
            try:
                if airline_username != username:
                    return None
                airline_query_set =  self.airline_company_dal.get_airline_by_username(username=username)
                for element in airline_query_set:
                    airline = element
                return airline
            except Exception as e:
                airlinefacade_logger.error(f"An error occurred while fetching airline: {e}")
                print(f"An error occurred while fetching airline: {e}")
                return None
        airlinefacade_logger.error('Dal is not accessible')
        raise AccessDeniedError
    

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['airline']))
    def get_user_by_user_id(self,request, id):
        if (self.check_access('user_dal', 'get_user_by_user_id')):
            try:
                user = self.user_dal.get_user_by_id(id=id)
                if user is None:
                    return None
                return user
            except Exception as e:
                airlinefacade_logger.error(f"An error occurred while fetching user: {e}")
                print(f"An error occurred while fetching user: {e}")
                return None
        else:
            airlinefacade_logger.error('Dal is not accessible')
            raise AccessDeniedError  