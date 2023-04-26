import pytest
from django.contrib.auth.models import User, Group
from peregrine_app.models import Customer
from peregrine_app.dal import GroupDAL
from peregrine_app.facades.anonymousfacade import AnonymousFacade
from unittest import mock



"""Testing add customer function"""
# General test for functionalty
@pytest.mark.django_db
def test_add_customer():
    facade = AnonymousFacade()
    data = {}
    user_data = {'username': 'fucktesting', 'email':'fucktesting@gmail.com', 'password1':'fucktesting', 'password2':'fucktesting'}
    customer = facade.add_customer(request=None, user_data=user_data, data=data)
    assert isinstance(customer, Customer)


# Tests error occurring while adding customer. 
@pytest.mark.django_db
def test_add_customer_error():
    facade = AnonymousFacade()
    request = None
    user_data = {'username': 'test', 'password1': 'test', 'password2': 'test'}
    data = {'name': 'Test Customer'}
    with pytest.raises(Exception):
        facade.add_customer(request, user_data, data)


# Tests transaction rollback in case of error.  
@pytest.mark.django_db
def test_transaction_rollback():
    request = None
    username = 'testuser'
    password = 'testpassword'
    user_data = {'username': username, 'email':'akmdsm@gmail.com', 'password1': password, 'password2': password}
    data = {'first_name': 'Test', 'last_name': 'User'}
    facade = AnonymousFacade()
    with pytest.raises(ValueError):
        with mock.patch.object(GroupDAL, 'get_userRole_by_role', side_effect=ValueError('User role does not exist/not found')):
            facade.add_customer(request=request, user_data=user_data, data=data)
    assert User.objects.filter(username=username).count() == 0
    assert Customer.objects.filter(first_name='Test').count() == 0

 





"""Testing login function"""

# Tests invalid credentials during login. 
@pytest.mark.django_db
def test_login_func():
    facade = AnonymousFacade()
    request = None
    username = 'invalid'
    password = 'invalid'
    assert facade.login_func(request, username=username, password=password) == {'error': 'Invalid credentials'}



# Tests creating token for user during login.
@pytest.mark.django_db  
def test_login_func_create_token():
        facade = AnonymousFacade()

        # Test with valid credentials
        valid_credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        result = facade.login_func(None, **valid_credentials)
        assert 'access_token' in result
        assert 'payload' in result
        assert result['payload']['username'] == valid_credentials['username']

        # Test with invalid credentials
        invalid_credentials = {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        }
        result = facade.login_func(None, **invalid_credentials)
        assert 'access_token' not in result
        assert 'error' in result
        assert result['error'] == 'Invalid credentials'

        # Test with empty credentials
        empty_credentials = {
            'username': '',
            'password': ''
        }
        result = facade.login_func(None, **empty_credentials)
        assert 'access_token' not in result
        assert 'error' in result
        assert result['error'] == 'Invalid credentials'


# Tests checking user roles and groups.  
@pytest.mark.django_db
def test_check_user_roles_and_groups():
    
    username = 'testuser'
    password = 'testpassword'
    user = User.objects.create_user(username=username, password=password)
    
    group = Group.objects.create(name='customer')
    user.groups.add(group)
    user.save()
    request = type('',(object,), {'method':'POST','user': user})()
    print(f"{user}")
    response = AnonymousFacade().login_func(request=request, username=username, password=password)
    assert response['payload']['roles'] == ['customer']




"""Testing Logout"""

@pytest.mark.django_db
    # Tests successful logout. 
def test_logout_func_success():
    facade = AnonymousFacade()
    request = None
    user = None
    assert facade.logout_func(request, user) == {'success': 'Successfully logged out.'}