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


"""Login/Logout Logger"""
loginout_logger = logging.getLogger('loginlogout')
loginout_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('peregrine_app/logs/api/loginlogout.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
loginout_logger.addHandler(handler)








