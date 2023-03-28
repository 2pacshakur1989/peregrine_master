from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.peregrine_api.api_serializers.admin_serializer import AdminSerializer
from peregrine_app.peregrine_api.api_serializers.user_serializer import UserSerializer

adminfacade = AdministratorFacade(user_group='admin')

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def admin(request):

    # GET REQUESTS
    if request.method == 'GET' :

        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)       
        if 'id' in request.query_params:
            # Handle 'get_airlines_by_country' for all users
            id = request.query_params['id']
            admin = adminfacade.get_admin_by_id(request=request, admin_id=id)
            serializer = AdminSerializer(admin)
            return Response(serializer.data)
        
        else:
            admins = adminfacade.get_all_admins(request=request)
            serializer = AdminSerializer(admins, many=True)
            return Response(serializer.data)
        
    if request.method == 'POST' :
         
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        user_serializer = UserSerializer(data=request.data)
        admin_serializer = AdminSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not admin_serializer.is_valid():
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if adminfacade.add_administrator(request=request, user_data=user_serializer.validated_data, data=admin_serializer.validated_data):
            return Response({"message": "Customer Created successfully","user_data":user_serializer.data ,"admin_data": admin_serializer.data}, status=status.HTTP_201_CREATED)


             

        
        
    