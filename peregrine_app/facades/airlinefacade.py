"""airlineFacade is the airline's "app" or we can call it permissions.
It inherits the generic get functions from FacadeBase. Initializing its constructor,
requests the permitted dals from the Father class (Facadebase) """

# Importing the right facade and the required utilities
from .facadebase import FacadeBase
from peregrine_app.exceptions import AccessDeniedError,CannotRemoveFlight
from datetime import timedelta,datetime
from peregrine_app.utils import check_countries



class AirlineFacade(FacadeBase):
    
    def __init__(self):
        super().__init__(dals=['airline_company_dal', 'flight_dal','user_dal','ticket_dal'])
        
    @property
    def accessible_dals(self):
        return [('airline_company_dal', ['update_airline_company']), ('flight_dal', ['get_flights_by_airline_company_id','add_flight','update_flight', 'remove_flight','get_flight_by_id']),('user_dal', ['update_user']),('ticket_dal', ['get_tickets_by_flight_id'])]


    def get_my_flights(self,airline_company_id):
        if self.check_access('flight_dal', 'get_flights_by_airline_company_id'):
            try:
                return self.flight_dal.get_flights_by_airline_company_id(airline_company_id=airline_company_id)
            except Exception as e:
                print(f"An error occurred while fetching flights: {e}")
                return None
        raise AccessDeniedError 

    def update_airline(self,id, data):
        if self.check_access('airline_company_dal', 'update_airline_company'):
            try:
                return self.airline_company_dal.update_airline_company(id=id ,data=data)
            except Exception as e:
                print(f"An error occurred while updating airline: {e}")
                return None
        else:
            raise AccessDeniedError
        
    def add_flight(self, data, airlinecompany):     # This is for the API
        if self.check_access('flight_dal', 'add_flight'):    
            try:
                airline_object = data['airline_company_id']
                if airlinecompany.id != airline_object.id:
                    return False
                return self.flight_dal.add_flight(data=data)
            except Exception as e:
                print(f"An error occurred while adding flight: {e}")
                return None
        else:
            raise AccessDeniedError
        
    # def add_flight(self, data):     # This is for the App
    #     if self.check_access('flight_dal', 'add_flight'):    
    #         try:
    #             return self.flight_dal.add_flight(data=data)
    #         except Exception as e:
    #             print(f"An error occurred while adding flight: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError

    def update_flight(self, flight_id, data ,airlinecompany):  # This is for API
        if (self.check_access('flight_dal', 'update_flight')) and (self.check_access('flight_dal', 'get_flight_by_id')):
            try:
                flight = self.flight_dal.get_flight_by_id(id=flight_id)
                data_airline_company= data['airline_company_id']
                if (flight.airline_company_id.id != airlinecompany.id) or (airlinecompany.id != data_airline_company.id):
                    return False
                return self.flight_dal.update_flight(flight_id=flight_id,data=data)
            except Exception as e:
                print(f"An error occurred while updating flight: {e}")
                return None
        else:
            raise AccessDeniedError


    # def update_flight(self, flight_id, data):  # This is for App
    #     if self.check_access('flight_dal', 'update_flight'):
    #         try:
    #             return self.flight_dal.update_flight(flight_id=flight_id,data=data)
    #         except Exception as e:
    #             print(f"An error occurred while updating flight: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError
            
    def remove_flight(self, flight_id, airlinecompany):  # This is for the Api
        if (self.check_access('flight_dal', 'remove_flight')) and (self.check_access('ticket_dal', 'get_tickets_by_flight_id')) and (self.check_access('flight_dal', 'get_flight_by_id')) and (self.check_access('flight_dal', 'get_flights_by_airline_company_id')) and (self.check_access('flight_dal', 'get_flight_by_id')):   
            try:
                flight = self.flight_dal.get_flight_by_id(id=flight_id)
                if flight is None:
                    return 0
                if flight.airline_company_id.id != airlinecompany.id:
                    return 1    # returning a cue value  (Cannot Remove Another Airline's Flight !)        
                tickets = self.ticket_dal.get_tickets_by_flight_id(flight_id=flight_id)
                if not tickets.exists():
                    return self.flight_dal.remove_flight(flight_id=flight_id)
                else:
                    return 2 # returning a cue value  (This flight has an on going active/pruchased tickets thus cannot be removed !)
            except Exception as e:
                print(f"An error occurred while removing flight: {e}")
                return None
        else:
            raise AccessDeniedError
        
    # def remove_flight(self, flight_id):   # This is for the App
    #     if (self.check_access('flight_dal', 'remove_flight')) and (self.check_access('ticket_dal', 'get_tickets_by_flight_id')):   
    #         try:
    #             tickets = self.ticket_dal.get_tickets_by_flight_id(flight_id=flight_id)
    #             if not tickets.exists():
    #                 return self.flight_dal.remove_flight(flight_id=flight_id)
    #             else:
    #                 raise CannotRemoveFlight
    #         except Exception as e:
    #             print(f"An error occurred while removing flight: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError
           
    def update_user(self,id, data):
        if self.check_access('user_dal', 'update_user'):
            try:
                return self.user_dal.update_user(id=id,data=data)
            except Exception as e:
                print(f"An error occurred while updating customer: {e}")
                return None
        else:
            raise AccessDeniedError