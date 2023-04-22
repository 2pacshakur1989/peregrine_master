"""Customer API view which includes , GET all customers (for the admin only), add customer,
which is for the admin, and anonymous only , remove customer (admin only), update customer(customer only)"""

from rest_framework.decorators import api_view
from peregrine_app.peregrine_api.api_serializers.customer_serializer import CustomerSerializer , DisplayCustomerSerializer
from peregrine_app.peregrine_api.api_serializers.user_serializer import UserSerializer,UpdateUserSerializer
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.facades.customerfacade import CustomerFacade
from peregrine_app.facades.anonymousfacade import AnonymousFacade
from peregrine_app.loggers import customer_logger


adminfacade = AdministratorFacade(user_group='admin')
customerfacade = CustomerFacade(user_group='customer')
anonymousfacade = AnonymousFacade()

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def customer(request):

    # GET REQUESTS 
    if request.method == 'GET':

        # This method is accessible only to the customer
        if 'id' in request.query_params:
            if not ((request.user.is_authenticated) and ((request.user.groups.filter(name='customer').exists()) or (request.user.groups.filter(name='admin').exists()))):
                customer_logger.info('Unauthorized attempt')
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            id = request.query_params['id']
            customer_instance = request.user.customer
            customer =  customerfacade.get_customer_by_id(request=request, customer_id=id, customer_instance=customer_instance)
            serializer = DisplayCustomerSerializer(customer)
            customer_logger.info(f"Get customer by id attempt - customer {request.user.customer.id}")
            return Response(serializer.data)
        
        if 'customer_id' in request.query_params:
            if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
                customer_logger.info('Unauthorized attempt')
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            id = request.query_params['customer_id']
          
            customer =  adminfacade.get_customer_by_id(request=request, customer_id=id)
            serializer = DisplayCustomerSerializer(customer)
            customer_logger.info(f"Get customer by id attempt - customer {request.user.administrator.id}")
            return Response(serializer.data)
        
        if 'user_id' in request.query_params:
            if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
                customer_logger.info('Unauthorized attempt')
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
            user_id = request.query_params['user_id']
            customer =  customerfacade.get_customer_by_user_id(request=request, id=user_id)
            user = customerfacade.get_user_by_user_id(request=request, id=user_id)
            customer_serializer = DisplayCustomerSerializer(customer)
            user_serializer = UserSerializer(user)
            customer_logger.info(f"Get customer by username attempt - customer {request.user.customer.id}")
            return Response({"user_data":user_serializer.data, "customer_data":customer_serializer.data})
        # if 'username' in request.query_params:
        #     if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
        #         customer_logger.info('Unauthorized attempt')
        #         return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        #     username = request.query_params['username']
        #     customer =  customerfacade.get_customer_by_username(request=request, username=username)
        #     user = customerfacade.get_user_by_username(request=request, username=username)
        #     customer_serializer = DisplayCustomerSerializer(customer)
        #     user_serializer = UserSerializer(user)
        #     customer_logger.info(f"Get customer by username attempt - customer {request.user.customer.id}")
        #     return Response({"user_data":user_serializer.data, "customer_data":customer_serializer.data})
        
        # This method is accessible only to the admin
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            customer_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        customers = adminfacade.get_all_customers(request=request)
        serializer = DisplayCustomerSerializer(customers, many=True)
        customer_logger.info(f"Get all customers attempt - admin {request.user.administrator.id}")
        return Response(serializer.data)
    

    # POST REQUESTS
    if request.method == 'POST':
        #This method is accessible to an anonymous user who wants to create a customer profile , and the admin
        if ((request.user.is_authenticated) and ((request.user.groups.filter(name='airline').exists()) or (request.user.groups.filter(name='customer').exists()))):
            customer_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        # Serializing the data
        customer_serializer = CustomerSerializer(data=request.data)
        user_serializer = UserSerializer(data=request.data)
        if not user_serializer.is_valid():
            customer_logger.error(user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not customer_serializer.is_valid():
            customer_logger.error(customer_serializer.errors)
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
        if anonymousfacade.add_customer(request=request, user_data=user_serializer.validated_data, data=customer_serializer.validated_data) is not None:
            customer_logger.info(f"Attempted create a new customer")
            # return Response({"message": "Customer Created successfully","user_data":user_serializer.data ,"customer_data": customer_serializer.data}, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_201_CREATED)



    # PUT REQUESTS
    if request.method == 'PATCH':
        # This method is accessible only for existing customers
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
            customer_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if not 'id' in request.query_params:
            customer_logger.info('Customer id must be provided')
            return Response("Customer id must be provided.", status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.customer.id) != request.query_params['id']:
            customer_logger.info('Customer is allowed to update its own details ONLY')
            return Response("Customer is allowed to update its own details ONLY", status=status.HTTP_403_FORBIDDEN)  
        user_id = request.user.customer.user_id.id
        currentpassword = request.user.password
        # Creating new serializer instances with the existing objects and partial=True (to allow the fields to be optional for update)
        data = request.data.copy()
        if 'current_password' in data and not data['current_password']:
            del data['current_password']
        if 'password1' in data and not data['password1']:
            del data['password1']
        if 'password2' in data and not data['password2']:
            del data['password2']
        
        user_serializer = UpdateUserSerializer(request.user, data=data, partial=True)
        customer_serializer = CustomerSerializer(request.user.customer, data=request.data)
        if not user_serializer.is_valid():
            customer_logger.error(user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not customer_serializer.is_valid():
            customer_logger.error(customer_serializer.errors)
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        if customerfacade.update_customer(request=request, customer_id=request.query_params['id'], user_id=user_id, user_data=user_serializer.validated_data, data=customer_serializer.validated_data, currentpassword=currentpassword) is not None:
            # Serializing the data again in order to present it
            customer_logger.info(f"Attempted update customer - customer {request.user.customer.id}")
            # return Response({"message": "Customer Updated successfully", "data": {"user": user_serializer.validated_data, "customer": customer_serializer.validated_data}}, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_304_NOT_MODIFIED)
 
    # DELETE REQUESTS
    if request.method == 'DELETE':
        # This method is accessible only for the admin
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            customer_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if not 'id' in request.query_params:
            customer_logger.info('Ticket id must be provided')
            return Response("Ticket id must be provided.", status=status.HTTP_400_BAD_REQUEST)
        customer_logger.info(f"Attempted remove customer - admin {request.user.administrator.id}")
        return Response(adminfacade.remove_customer(request=request ,customer_id=request.query_params['id']))
