import logging



"""DAL Logger"""
#################################
dal_logger = logging.getLogger('dal')
dal_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/dal/dal.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
dal_logger.addHandler(handler)










"""Facades Loggers :"""
#################################

"""Facadebase logger"""
facadebase_logger = logging.getLogger('facadebase')
facadebase_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/facades/facadebase.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
facadebase_logger.addHandler(handler)


"""AnonymousFacade logger"""
anonymousfacade_logger = logging.getLogger('anonymousfacade')
anonymousfacade_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/facades/anonymousfacade.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
anonymousfacade_logger.addHandler(handler)


"""CustomerFacade logger"""
customerfacade_logger = logging.getLogger('customerfacade')
customerfacade_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/facades/customerfacade.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
customerfacade_logger.addHandler(handler)


"""AirlineFacade logger"""
airlinefacade_logger = logging.getLogger('airlinefacade')
airlinefacade_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/facades/airlinefacade.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
airlinefacade_logger.addHandler(handler)


"""AdminFacade logger"""
adminfacade_logger = logging.getLogger('adminfacade')
adminfacade_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/facades/adminfacade.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
adminfacade_logger.addHandler(handler)









""" API Loggers :"""
#################################

"""Ticket logger"""
ticket_logger = logging.getLogger('ticket')
ticket_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/api/ticket.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
ticket_logger.addHandler(handler)


"""Login/Logout logger"""
loginout_logger = logging.getLogger('loginlogout')
loginout_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/api/loginlogout.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
loginout_logger.addHandler(handler)


"""Flight logger"""
flight_logger = logging.getLogger('flight')
flight_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/api/flight.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
flight_logger.addHandler(handler)


"""Customer logger"""
customer_logger = logging.getLogger('customer')
customer_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/api/customer.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
customer_logger.addHandler(handler)


"""Country logger"""
country_logger = logging.getLogger('country')
country_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/api/country.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
country_logger.addHandler(handler)


""""Airline logger"""
airline_logger = logging.getLogger('airline')
airline_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/api/airline.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
airline_logger.addHandler(handler)


"""Admin logger"""
admin_logger = logging.getLogger('admin')
admin_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/api/admin.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
admin_logger.addHandler(handler)






