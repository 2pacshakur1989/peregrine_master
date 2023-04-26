import pytest
from django.contrib.auth.models import User, Group
from peregrine_app.models import Customer ,Flight
from peregrine_app.dal import GroupDAL
from peregrine_app.models import Flight, AirlineCompany, Country
from peregrine_app.facades.airlinefacade import AirlineFacade
from peregrine_app.exceptions import AccessDeniedError



# Creating a fixture to test with
@pytest.fixture
def test_data():
    user_data = {'username': 'test', 'email':'jnkwe@gmail.com', 'password': 'test'}
    user = User.objects.create(**user_data)

    country_data = {'name': 'Fucktonia'}
    country = Country.objects.create(**country_data)

    airline_data = {'name': 'AirFrance', 'country_id': country, 'user_id': user}
    airline = AirlineCompany.objects.create(**airline_data)

    flight_data = {'airline_company_id': airline, 'origin_country_id': country, 'destination_country_id': country,  'departure_time': '2022-01-01 00:00:00', 'landing_time': '2022-01-01 00:00:00', 'remaining_tickets':789}
    flight = Flight.objects.create(**flight_data)
    
    return {'user': user, 'country': country, 'airline': airline, 'flight':flight}



# Tests that the constructor initializes the object with a valid user group. 
@pytest.mark.django_db
def test_init_with_valid_user_group():
    # Arrange
    user_group = 'airline'
    # Act
    facade = AirlineFacade(user_group)
    # Assert
    assert facade._user_group == user_group


# Tests that the accessible_dals property returns a list of tuples containing the correct DALs and methods. 
@pytest.mark.django_db
def test_accessible_dals():
    # Arrange
    facade = AirlineFacade(user_group='airline')
    # Act
    accessible_dals = facade.accessible_dals
    # Assert
    assert accessible_dals == [('airline_company_dal', ['update_airline_company', 'get_airline_company_by_id', 'get_airline_by_username','get_airline_by_user_id']), ('flight_dal', ['get_flights_by_airline_company_id','add_flight','update_flight', 'remove_flight','get_flight_by_id']),('user_dal', ['update_user', 'get_user_by_user_id']),('ticket_dal', ['get_tickets_by_flight_id']), ('country_dal', ['get_country_by_id'])]


# Tests that the constructor raises a ValueError when initialized with an invalid user group. 
@pytest.mark.django_db
def test_init_with_invalid_user_group():
    # Arrange
    user_group = 'invalid'
    # Act & Assert
    with pytest.raises(ValueError):
        AirlineFacade(user_group)


# Tests that the get_my_flights method raises an exception when given invalid input. 
@pytest.mark.django_db
def test_get_my_flights_with_invalid_input():
    # Arrange
    facade = AirlineFacade(user_group='airline')
    request = None
    airline_company_id = None
    # Act & Assert
    with pytest.raises(Exception):
        facade.get_my_flights(request, airline_company_id)


# Tests that the get_my_flights method returns the expected output when given valid input.
## TEST NOT WORKING PROPERLY
@pytest.mark.django_db
def test_get_my_flights_valid(test_data):
    # Arrange
    user = test_data['user']
    airline = test_data['airline']
    airline_facade = AirlineFacade(user_group='airline')
    request = type('http://localhost:8000/api/flights/?my',(object,), {'method':'GET','user': user})()
    # Act
    result = airline_facade.get_my_flights(request=request, airline_company_id=airline.id)
    # Assert
    assert result


# Tests that the update_airline method returns the expected output when given valid input. 
@pytest.mark.django_db
def test_update_airline_with_valid_input(test_data):
    # Arrange
    facade = AirlineFacade(user_group='airline')
    user = test_data['user']
    airline = test_data['airline']
    # airline =''
    country = test_data['country']
    airline_data = {'name': 'AirFrance', 'country_id': country, 'user_id': user}
    user_data = {'username': 'test', 'email':'jnkwe@gmail.com', 'password': 'test'}
    current_password = 'test'
    request = type('',(object,), {'method':'PATCH','user': user})()
    # Act
    result = facade.update_airline(request=request, airline_company_id=airline.id, user_id=user.id, user_data=user_data, data=airline_data, currentpassword=current_password)
    # Assert
    assert result is not None

# Tests that the update_airline method raises an exception when given invalid input. 
"""NOT A GOOD FUNCTION"""
@pytest.mark.django_db
def test_update_airline_with_invalid_input(test_data):
    # Arrange
    facade = AirlineFacade(user_group='airline')
    user = test_data['user']
    airline = test_data['airline']
    # airline =''
    country = test_data['country']
    airline_data = {'name': 'AirFrance', 'country_id': country, 'user_id': user}
    user_data = {'username': 'test', 'email':'jnkwe@gmail.com', 'password': 'test'}
    current_password = 'wetwrwtwry'
    request = type('',(object,), {'method':'PATCH','user': user})()

    # Act & Assert
    with pytest.raises(Exception):
        facade.update_airline(request=request, airline_company_id=airline.id, user_id=user.id, user_data=user_data, data=airline_data, currentpassword=current_password)

# Tests that the add_flight method returns the expected output when given valid input. 
@pytest.mark.django_db
def test_add_flight_with_valid_input(test_data):
    # Arrange
    airline = test_data['airline']
    user = test_data['user']

    country_data1 = {'name': 'Cuntonia'} 
    country1 = Country.objects.create(**country_data1)
    country1.save()

    country_data2 = {'name': 'Shitonia'}
    country2 = Country.objects.create(**country_data2)
    country2.save()

    facade = AirlineFacade(user_group='airline')
    request = None
    data = {'airline_company_id': airline , 'departure_time': '2022-01-01 00:00:00', 'landing_time': '2022-01-01 00:00:00', 'origin_country_id': country1, 'destination_country_id':country2 , 'remaining_tickets': 100}

    request = type('',(object,), {'method':'POST','user':user })()
    # Act
    result = facade.add_flight(request=request, data=data, airlinecompany=airline)

    # Assert
    assert result is not None

# Tests that the add_flight method raises an exception when given invalid input. 
@pytest.mark.django_db
def test_add_flight_with_invalid_input(test_data):
    # Arrange
    airline = test_data['airline']
    # user = test_data['user']

    country_data1 = {'name': 'Cuntonia'} 
    country1 = Country.objects.create(**country_data1)
    country1.save()

    country_data2 = {'name': 'Shitonia'}
    country2 = Country.objects.create(**country_data2)
    country2.save()

    facade = AirlineFacade(user_group='airline')
    request = None
    data = {}

    request = type('',(object,), {'method':'POST' })()

    # Act & Assert
    with pytest.raises(Exception):
        facade.add_flight(request=request, data=data, airlinecompany=airline)


# Tests that the update_flight method returns the expected output when given valid input. 
@pytest.mark.django_db
def test_update_flight_with_valid_input(test_data):
    # Arrange
    facade = AirlineFacade(user_group='airline')
    airline = test_data['airline']
    user = test_data['user']
    flight = test_data['flight']

    country_data1 = {'name': 'Cuntonia'} 
    country1 = Country.objects.create(**country_data1)
    country1.save()

    country_data2 = {'name': 'Shitonia'}
    country2 = Country.objects.create(**country_data2)
    country2.save()

    facade = AirlineFacade(user_group='airline')
    request = None
    data = {}

    
    request = type('',(object,), {'method':'PATCH', 'user': user})()


    data = {'airline_company_id': airline, 'departure_time': '2022-01-01 00:00:00', 'landing_time': '2022-01-01 00:00:00', 'origin_country_id': country1, 'destination_country_id': country2, 'remaining_tickets': 100}

    # Act
    result = facade.update_flight(request=request, flight_id=flight, data=data, airlinecompany=airline)

    # Assert
    assert result is not None

# Tests that the update_flight method raises an exception when given invalid input. 
@pytest.mark.django_db
def test_update_flight_with_invalid_input():
    # Arrange
    facade = AirlineFacade(user_group='airline')
    request = None
    flight_id = 1
    data = {}
    airlinecompany = 2

    # Act & Assert
    with pytest.raises(Exception):
        facade.update_flight(request, flight_id, data, airlinecompany)

# Tests that the remove_flight method returns the expected output when given valid input. 
@pytest.mark.django_db
def test_remove_flight_with_valid_input():
    # Arrange
    facade = AirlineFacade(user_group='airline')
    request = None
    flight_id = 1
    airlinecompany = 2

    # Act
    result = facade.remove_flight(request, flight_id, airlinecompany)

    # Assert
    assert result is not None
    assert result is False or result is True

