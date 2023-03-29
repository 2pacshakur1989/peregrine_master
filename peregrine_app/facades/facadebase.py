""" FacadeBase is the base facade layer, which initializes the DALs in its constructor.
The DALs are assigend to variables. 
Facadebase has generic get methods which are authorized (permitted) for all users (including 
an anonymous app user)"""

""" The "transaction.atomic()" method makes sure that in case of encountering, a problem
of adding one of the 2 (or user_form , or customer_form) then it won't add anything to the DB
"""
# Importing the DAL and the needed utilities
from peregrine_app.dal import TokenDAL, AdministratorDAL,UserDAL,FlightDAL,TicketDAL,CountryDAL,CustomerDAL,AirlineCompanyDAL,GroupDAL
from abc import abstractmethod
from peregrine_app.loggers import facadebase_logger

    
class FacadeBase:

    def __init__(self, dals=None):

        self.administrator_dal = AdministratorDAL()
        self.user_dal = UserDAL()
        self.flight_dal = FlightDAL()
        self.ticket_dal = TicketDAL()
        self.country_dal = CountryDAL()
        self.customer_dal = CustomerDAL()
        self.group_dal = GroupDAL()
        self.airline_company_dal = AirlineCompanyDAL()

        if dals is not None:
            for dal in dals:
                if dal == "administrator_dal":
                    self.administrator_dal = AdministratorDAL()
                elif dal == "user_dal":
                    self.user_dal = UserDAL()
                elif dal == "flight_dal":
                    self.flight_dal = FlightDAL()
                elif dal == "ticket_dal":
                    self.ticket_dal = TicketDAL()
                elif dal == "country_dal":
                    self.country_dal = CountryDAL()
                elif dal == "customer_dal":
                    self.customer_dal = CustomerDAL()
                elif dal == "user_role_dal":
                    self.group_dal = GroupDAL()
                elif dal == "airline_company_dal":
                    self.airline_company_dal = AirlineCompanyDAL()
                elif dal == "token_dal":
                    self.token_dal = TokenDAL()


        """This method is abstract since it MUST be implemented in all other facaedes,
     as this method defines the dals, that are accessible to the specific inheriting Facade """
    @abstractmethod    
    def accessible_dals(self):
        pass

        """This method's parameters (dal_name , method_name), will be set in the other facades.
        The method provides another layer of securing the permissions between different facades,
        it does so by making sure the dal_name, and method_name, are allowed in the accessible dals,
        if so, the code will continue and we'll enter the function. else wise an error will be raised"""    
    def check_access(self, dal_name, method_name):   
        for dal in self.accessible_dals:
            if (dal[0] == dal_name) and (method_name in dal[1]):
                return True
        return False


    def get_all_flights(self, request): 

            return self.flight_dal.get_all_flights()   
    
    def get_flight_by_id(self, request, id):
        try:
            return self.flight_dal.get_flight_by_id(id=id)
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching flight: {e}")
            print(f"An error occurred while fetching flight: {e}")
            return None
        
    def get_flights_by_origin_country_id(self, request, origin_country_id):
        try:
            return self.flight_dal.get_flights_by_origin_country_id(origin_country_id=origin_country_id)
        except Exception as e:
            facadebase_logger.error(f"facade : An error occurred while fetching flights: {e}")
            print(f"facade : An error occurred while fetching flights: {e}")
            return None
        
    def get_flights_by_destination_country_id(self, request, destination_country_id):
        try:
            return self.flight_dal.get_flights_by_destination_country_id(destination_country_id=destination_country_id)
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching flights: {e}")
            print(f"An error occurred while fetching flights: {e}")
            return None

    def get_arrival_flights_by_country_id(self, request, country_id):
        try:
            return self.flight_dal.get_arrival_flights_by_country_id(country_id=country_id)   
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching flights: {e}")
            print(f"An error occurred while fetching flights: {e}")
            return None

    def get_departure_flights_by_country_id(self, request, country_id):
        try:
            return self.flight_dal.get_departure_flights_by_country_id(country_id=country_id)   
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching flights: {e}")
            print(f"An error occurred while fetching flights: {e}")
            return None       
        
    def get_flights_by_departure_date(self, request, departure_time):
        try:
            return self.flight_dal.get_flights_by_departure_date(departure_time=departure_time)
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching flights: {e}")
            print(f"An error occurred while fetching flights: {e}")
            return None

    def get_flights_by_landing_date(self, request, landing_time):
        try:
            return self.flight_dal.get_flights_by_landing_date(landing_time=landing_time)
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching flights: {e}")
            print(f"An error occurred while fetching flights: {e}")
            return None
        
    def get_flights_by_airline_company(self, request, airline_company_id):
        try:
            return self.flight_dal.get_flights_by_airline_company_id(airline_company_id=airline_company_id)
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching flights: {e}")
            print(f"An error occurred while fetching flights: {e}")
            return None       
    
    def get_all_airlines(self, request):

            return self.airline_company_dal.get_all_airline_companies()
    
    def get_airline_by_id(self, request, id):
        try:
            return self.airline_company_dal.get_airline_company_by_id(id=id)
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching airline: {e}")
            print(f"An error occurred while fetching airline: {e}")
            return None
    
    def get_airline_by_country(self, request, country_id):
        try:
            return self.airline_company_dal.get_airlines_by_country(country_id=country_id)
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching airlines: {e}")
            print(f"An error occurred while fetching airlines: {e}")
            return None
     
    def get_all_countries(self, request):

            return self.country_dal.get_all_countries()
   
    def get_country_by_id(self, request, country_id):
        try:
            return self.country_dal.get_country_by_id(country_id=country_id)
        except Exception as e:
            facadebase_logger.error(f"An error occurred while fetching country: {e}")
            print(f"An error occurred while fetching country: {e}")
            return None











































