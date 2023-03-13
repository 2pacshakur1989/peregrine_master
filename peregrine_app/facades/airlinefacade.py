from .facadebase import FacadeBase
from peregrine_app.exceptions import AccessDeniedError,CannotRemoveFlight




# class AirlineFacade:
    
#     def __init__(self):
#         self.facade_base = FacadeBase(['airline_company_dal', 'flight_dal','user_dal'])
#         self.accessible_dals = [('airline_company_dal', ['update_airline_company']), ('flight_dal', ['get_flights_by_airline_company_id', 'add_flight', 'update_flight', 'remove_flight']),('user_dal', ['update_user'])]

    # def __getattr__(self, name):
    #     for dal, funcs in self.accessible_dals:
    #         if name in funcs:
    #             return getattr(getattr(self.facade_base, dal), name)
    #     raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    # def check_access(self, dal_name, method_name):
    #     for dal in self.accessible_dals:
    #         if dal[0] == dal_name and method_name in dal[1]:
    #             return True
    #     return False

    # def get_my_flights(self,airline_company_id):
    #     if self.check_access('flight_dal', 'get_flights_by_airline_company_id'):
    #         try:
    #             return self.facade_base.flight_dal.get_flights_by_airline_company_id(airline_company_id=airline_company_id)
    #         except Exception as e:
    #             print(f"An error occurred while fetching flights: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError 

    # def update_airline(self,id, data):
    #     if self.check_access('airline_company_dal', 'update_airline_company'):
    #         try:
    #             return self.facade_base.airline_company_dal.update_airline_company(id=id ,data=data)
    #         except Exception as e:
    #             print(f"An error occurred while updating airline: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError
        
    # def add_flight(self, data):
    #     if self.check_access('flight_dal', 'add_flight'):
    #         try:
    #             return self.facade_base.flight_dal.add_flight(data=data)
    #         except Exception as e:
    #             print(f"An error occurred while adding flight: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError
        
    # def update_flight(self, flight_id, data):
    #     if self.check_access('flight_dal', 'update_flight'):
    #         try:
    #             return self.facade_base.flight_dal.update_flight(flight_id=flight_id,data=data)
    #         except Exception as e:
    #             print(f"An error occurred while updating flight: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError
            
    # def remove_flight(self, flight_id):
    #     if self.check_access('flight_dal', 'remove_flight'):   
    #         try:
    #             return self.facade_base.flight_dal.remove_flight(flight_id=flight_id)
    #         except Exception as e:
    #             print(f"An error occurred while removing flight: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError
        
    # def update_user(self,id, data):
    #     if self.check_access('user_dal', 'update_user'):
    #         try:
    #             return self.facade_base.user_dal.update_user(id=id,data=data)
    #         except Exception as e:
    #             print(f"An error occurred while updating customer: {e}")
    #             return None
    #     else:
    #         raise AccessDeniedError









############ DO NOT CROSS UP #############





# class AirlineFacade(FacadeBase):
    
#     def __init__(self):
#         super().__init__(dals=['airline_company_dal', 'flight_dal','user_dal'])
#         self.accessible_dals = [('airline_company_dal', ['update_airline_company']), ('flight_dal', ['get_flights_by_airline_company_id', 'add_flight', 'update_flight', 'remove_flight']),('user_dal', ['update_user'])]


#     def __getattr__(self, name):
#         for dal, funcs in self.accessible_dals:
#             if name in funcs:
#                 return getattr(getattr(self, dal), name)
#         raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
#     def check_access(self, dal_name, method_name):
#         for dal in self.accessible_dals:
#             if dal[0] == dal_name and method_name in dal[1]:
#                 return True
#         return False

#     def get_my_flights(self,airline_company_id):
#         if self.check_access('flight_dal', 'get_flights_by_airline_company_id'):
#             try:
#                 return self.flight_dal.get_flights_by_airline_company_id(airline_company_id=airline_company_id)
#             except Exception as e:
#                 print(f"An error occurred while fetching flights: {e}")
#                 return None
#         else:
#             raise AccessDeniedError 

#     def update_airline(self,id, data):
#         if self.check_access('airline_company_dal', 'update_airline_company'):
#             try:
#                 return self.airline_company_dal.update_airline_company(id=id ,data=data)
#             except Exception as e:
#                 print(f"An error occurred while updating airline: {e}")
#                 return None
#         else:
#             raise AccessDeniedError
        
#     def add_flight(self, data):
#         if self.check_access('flight_dal', 'add_flight'):
#             try:
#                 return self.flight_dal.add_flight(data=data)
#             except Exception as e:
#                 print(f"An error occurred while adding flight: {e}")
#                 return None
#         else:
#             raise AccessDeniedError
        
#     def update_flight(self, flight_id, data):
#         if self.check_access('flight_dal', 'update_flight'):
#             try:
#                 return self.flight_dal.update_flight(flight_id=flight_id,data=data)
#             except Exception as e:
#                 print(f"An error occurred while updating flight: {e}")
#                 return None
#         else:
#             raise AccessDeniedError
            
#     def remove_flight(self, flight_id):
#         if self.check_access('flight_dal', 'remove_flight'):   
#             try:
#                 return self.flight_dal.remove_flight(flight_id=flight_id)
#             except Exception as e:
#                 print(f"An error occurred while removing flight: {e}")
#                 return None
#         else:
#             raise AccessDeniedError
        
#     def update_user(self,id, data):
#         if self.check_access('user_dal', 'update_user'):
#             try:
#                 return self.user_dal.update_user(id=id,data=data)
#             except Exception as e:
#                 print(f"An error occurred while updating customer: {e}")
#                 return None
#         else:
#             raise AccessDeniedError










#################################################







class AirlineFacade(FacadeBase):
    
    def __init__(self):
        super().__init__(dals=['airline_company_dal', 'flight_dal','user_dal','ticket_dal'])
        
    @property
    def accessible_dals(self):
        return [('airline_company_dal', ['update_airline_company']), ('flight_dal', ['get_flights_by_airline_company_id','add_flight','update_flight', 'remove_flight']),('user_dal', ['update_user']),('ticket_dal', ['get_tickets_by_flight_id'])]


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
        
    def add_flight(self, data):
        if self.check_access('flight_dal', 'add_flight'):
            if (data['departure_time'] < data['landing_time']) and (data['origin_country_id']!=data['destination_country_id']):
                try:
                    return self.flight_dal.add_flight(data=data)
                except Exception as e:
                    print(f"An error occurred while adding flight: {e}")
                    return None
            else:
                raise ValueError
        else:
            raise AccessDeniedError

        
    def update_flight(self, flight_id, data):
        if self.check_access('flight_dal', 'update_flight'):
            try:
                return self.flight_dal.update_flight(flight_id=flight_id,data=data)
            except Exception as e:
                print(f"An error occurred while updating flight: {e}")
                return None
        else:
            raise AccessDeniedError
            
    def remove_flight(self, flight_id):
        if (self.check_access('flight_dal', 'remove_flight')) and (self.check_access('ticket_dal', 'get_tickets_by_flight_id')):   
            try:
                tickets = self.ticket_dal.get_tickets_by_flight_id(flight_id=flight_id)
                if tickets == None:
                    return self.flight_dal.remove_flight(flight_id=flight_id)
                else:
                    raise CannotRemoveFlight
            except Exception as e:
                print(f"An error occurred while removing flight: {e}")
                return None
        else:
            raise AccessDeniedError
        
    
    def update_user(self,id, data):
        if self.check_access('user_dal', 'update_user'):
            try:
                return self.user_dal.update_user(id=id,data=data)
            except Exception as e:
                print(f"An error occurred while updating customer: {e}")
                return None
        else:
            raise AccessDeniedError