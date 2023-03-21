from rest_framework.decorators import api_view
from peregrine_app.peregrine_api.api_serializers.customer_serializer import CustomerSerializer
from peregrine_app.peregrine_api.api_serializers.user_serializer import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.facades.customerfacade import CustomerFacade

""" we are going to create a customer API view which includes , GET all customers (for the admin only), add customer,
which is for the admin, and anonymous only , remove customer (admin only), update customer(customer only)"""

adminfacade = AdministratorFacade()
customerfacade = CustomerFacade()

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def customer(request, id=None):

    # GET REQUESTS 
    if request.method == 'GET':
        # This method is accessible only to the admin
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        customers = adminfacade.get_all_customers()
        if customers is None:
            return Response("No customers found.", status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    

    # POST REQUESTS
    if request.method == 'POST':
        #This method is accessible to an anonymous user who wants to create a customer profile , and the admin
        if ((request.user.is_authenticated) and ((request.user.groups.filter(name='airline').exists()) or (request.user.groups.filter(name='customer').exists()))):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        customer_serializer = CustomerSerializer(data=request.data)
        user_serializer = UserSerializer(data=request.data)
        if (customer_serializer.is_valid()) and (user_serializer.is_valid()):
        # Use validated data instead of request.data
            user_data = {
                'username': user_serializer.validated_data['username'],
                'email': user_serializer.validated_data['email'],
                'password': user_serializer.validated_data['password1']
            }
            customer_data = {
                'first_name': customer_serializer.validated_data['first_name'],
                'last_name': customer_serializer.validated_data['last_name'],
                'address': customer_serializer.validated_data['address'],
                'phone_no': customer_serializer.validated_data['phone_no'],
                'credit_card_no': customer_serializer.validated_data['credit_card_no'],
            }            
            new_customer = adminfacade.add_customer(user_data=user_data, data=customer_data)
            customer_serializer = CustomerSerializer(new_customer)
            user_serializer = UserSerializer(new_customer)
            return Response({"message": "Customer Created successfully", "data": customer_serializer.data}, status=status.HTTP_201_CREATED)
        # The errors were done this way because in order to return 2 different serializers errors , You must call is_valid() before accessing .errors.
        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)
        if not customer_serializer.is_valid():
            errors.update(customer_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


    # PATCH REQUESTS
    if request.method == 'PATCH':
        # This method is accessible only for existing customers
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='customer').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if str(request.user.customer.id) != id:
            return Response("Customer is allowed to update its own details ONLY", status=status.HTTP_403_FORBIDDEN)  
        user_id = request.user.customer.user_id.id

        # Create new serializer instances with the existing objects and partial=True
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        customer_serializer = CustomerSerializer(request.user.customer, data=request.data, partial=True)

        if user_serializer.is_valid():
            user_data = {
            }
        # Use validated data instead of request.data
            if 'username' in request.data:
                user_data.update({'username': user_serializer.validated_data['username']})
            if 'email' in request.data:
                user_data.update({'email': user_serializer.validated_data['email']})
            if 'password1' in request.data:
                user_data.update({'password1': user_serializer.validated_data['password1']})  
            if 'password2' in request.data:
                user_data.update({'password1': user_serializer.validated_data['password2']})    
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if customer_serializer.is_valid():
            customer_data = {}

            if 'first_name' in request.data:
                customer_data.update({'first_name': customer_serializer.validated_data['first_name']})
            if 'last_name' in request.data:
                customer_data.update({'last_name': customer_serializer.validated_data['last_name']})
            if 'address' in request.data:
                customer_data.update({'address': customer_serializer.validated_data['address']})
            if 'phone_no' in request.data:
                customer_data.update({'phone_no': customer_serializer.validated_data['phone_no']})
            if 'credit_card_no' in request.data:
                customer_data.update({'credit_card_no': customer_serializer.validated_data['credit_card_no']}) 
        else:
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        customerfacade.update_customer(customer_id=id, user_id=user_id, user_data=user_data, data=customer_data)

        updated_user_obj = request.user
        updated_customer_obj = request.user.customer
        updated_user_serializer = UserSerializer(updated_user_obj)
        updated_customer_serializer = CustomerSerializer(updated_customer_obj)

        return Response({"message": "Customer Updated successfully", "data": {"user": updated_user_serializer.data, "customer": updated_customer_serializer.data}}, status=status.HTTP_201_CREATED)

        ##### SOLVE THE ISSUE OF THE DISPLAYED DATA !!!!!

 
    # DELETE REQUESTS
    if request.method == 'DELETE':
        # This method is accessible only for the admin
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if adminfacade.remove_customer(customer_id=id) == True:
            return Response("Customer removed succesfully",  status=status.HTTP_202_ACCEPTED)
        elif adminfacade.remove_customer(customer_id=id) == 3:         
            return Response("This customer has an on going active ticket thus cannot be deleted")
        elif adminfacade.remove_customer(customer_id=id) == 4:
            return Response("Customer not found")

         
    
