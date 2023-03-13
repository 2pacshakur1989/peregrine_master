from .facadebase import FacadeBase
from peregrine_app.exceptions import AccessDeniedError

# class CustomerFacade:

#     def __init__(self):
#         self.facade_base = FacadeBase(['customer_dal', 'ticket_dal'])
#         self.accessible_dals = [('customer_dal', ['update_customer','get_customer_by_id']), ('ticket_dal', ['add_ticket', 'remove_ticket', 'get_ticket_by_id']),('user_dal', ['update_user'])]
    
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
    
#     def get_customer_by_id(self, customer_id):
#         if self.check_access('customer_dal', 'get_customer_by_id'):
#             try:
#                 return self.facade_base.customer_dal.get_customer_by_id(customer_id=customer_id)
#             except Exception as e:
#                 print(f"An error occurred while updating customer: {e}")
#                 return None
#         else:
#             raise AccessDeniedError
            
#     def update_customer(self, customer_id, data):
#         if self.check_access('customer_dal', 'update_customer'):
#             try:
#                 return self.facade_base.customer_dal.update_customer(customer_id=customer_id, data=data)
#             except Exception as e:
#                 print(f"An error occurred while updating customer: {e}")
#                 return None
#         else:
#             raise AccessDeniedError

#     def add_ticket(self, data):
#         if self.check_access('ticket_dal', 'add_ticket'):
#             try:
#                 return self.facade_base.ticket_dal.add_ticket(data=data)
#             except Exception as e:
#                 print(f"An error occurred while purchasing ticket: {e}")
#                 return None
#         else:
#             raise AccessDeniedError

#     def remove_ticket(self, id):
#         if self.check_access('ticket_dal', 'remove_ticket'):
#             try:
#                 return self.facade_base.ticket_dal.remove_ticket(id=id)
#             except Exception as e:
#                 print(f"An error occurred while removing ticket: {e}")
#                 return None
#         else:
#             raise AccessDeniedError

#     def get_my_tickets(self, customer_id):
#         if self.check_access('ticket_dal', 'get_ticket_by_id'):
#             try:
#                 return self.facade_base.ticket_dal.get_tickets_by_customer_id(customer_id=customer_id)
#             except Exception as e:
#                 print(f"An error occurred while fetching tickets: {e}")
#                 return None
#         else:
#             raise AccessDeniedError
        
#     def update_user(self,id, data):
#         if self.check_access('user_dal', 'update_user'):
#             try:
#                 return self.facade_base.user_dal.update_user(id=id,data=data)
#             except Exception as e:
#                 print(f"An error occurred while updating customer: {e}")
#                 return None
#         else:
#             raise AccessDeniedError








########## DO NOT CROSS UP ###########


class CustomerFacade(FacadeBase):

    def __init__(self):
        super().__init__(dals=['customer_dal', 'ticket_dal'])
    
    @property
    def accessible_dals(self):
        return [('customer_dal', ['update_customer','get_customer_by_id']), ('ticket_dal', ['add_ticket', 'remove_ticket', 'get_ticket_by_id']),('user_dal', ['update_user'])]
    
    
    def get_customer_by_id(self, customer_id):
        if self.check_access('customer_dal', 'get_customer_by_id'):
            try:
                return self.customer_dal.get_customer_by_id(customer_id=customer_id)
            except Exception as e:
                print(f"An error occurred while updating customer: {e}")
                return None
        else:
            raise AccessDeniedError
            
    def update_customer(self, customer_id, data):
        if self.check_access('customer_dal', 'update_customer'):
            try:
                return self.customer_dal.update_customer(customer_id=customer_id, data=data)
            except Exception as e:
                print(f"An error occurred while updating customer: {e}")
                return None
        else:
            raise AccessDeniedError

    def add_ticket(self, data):
        if self.check_access('ticket_dal', 'add_ticket'):
            try:
                return self.ticket_dal.add_ticket(data=data)
            except Exception as e:
                print(f"An error occurred while purchasing ticket: {e}")
                return None
        else:
            raise AccessDeniedError

    def remove_ticket(self, id):
        if self.check_access('ticket_dal', 'remove_ticket'):
            try:
                return self.ticket_dal.remove_ticket(id=id)
            except Exception as e:
                print(f"An error occurred while removing ticket: {e}")
                return None
        else:
            raise AccessDeniedError

    def get_my_tickets(self, customer_id):
        if self.check_access('ticket_dal', 'get_ticket_by_id'):
            try:
                return self.ticket_dal.get_tickets_by_customer_id(customer_id=customer_id)
            except Exception as e:
                print(f"An error occurred while fetching tickets: {e}")
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