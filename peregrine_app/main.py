from peregrine_app.facades.customerfacade import CustomerFacade


if __name__ == '__main__':
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    # ...

    customer_facade = CustomerFacade(user_group='customer')
    customer_facade.update_customer(data={...})
