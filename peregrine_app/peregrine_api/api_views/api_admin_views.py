from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from peregrine_app.facades.adminfacade import AdministratorFacade
from peregrine_app.peregrine_api.api_serializers.admin_serializer import AdminSerializer, DisplayAdminSerializer
from peregrine_app.peregrine_api.api_serializers.user_serializer import UserSerializer
from peregrine_app.loggers import admin_logger

adminfacade = AdministratorFacade(user_group='admin')

@api_view(['GET', 'POST', 'DELETE'])
def admin(request):

    # GET REQUESTS
    if request.method == 'GET' :

        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
                return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)       
        if 'id' in request.query_params:
            # Handle 'get_airlines_by_country' for all users
            id = request.query_params['id']
            admin = adminfacade.get_admin_by_id(request=request, admin_id=id)
            serializer = DisplayAdminSerializer(admin)
            admin_logger.info('Get admin by id attempt')
            return Response(serializer.data)
        
        else:
            admins = adminfacade.get_all_admins(request=request)
            serializer = DisplayAdminSerializer(admins, many=True)
            admin_logger.info('Get all admins attempt')
            return Response(serializer.data)


    # POST REQUESTS   
    if request.method == 'POST' :
         
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            admin_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        user_serializer = UserSerializer(data=request.data)
        admin_serializer = AdminSerializer(data=request.data)
        if not user_serializer.is_valid():
            admin_logger.error(user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not admin_serializer.is_valid():
            admin_logger.error(admin_serializer.errors)
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if adminfacade.add_administrator(request=request, user_data=user_serializer.validated_data, data=admin_serializer.validated_data):
            admin_logger.info(f"Attempted add admin - admin {request.user.administrator.id}")
            return Response({"message": "Admin Created successfully","user_data":user_serializer.data ,"admin_data": admin_serializer.data}, status=status.HTTP_201_CREATED)


    # DELETE REQUESTS
    if request.method == 'DELETE' :
        if not ((request.user.is_authenticated) and (request.user.groups.filter(name='admin').exists())):
            admin_logger.info('Unauthorized attempt')
            return Response("Authentication credentials not provided.", status=status.HTTP_401_UNAUTHORIZED)
        if not 'id' in request.query_params:
            admin_logger.info('Airline id must be provided')
            return Response("Airline id must be provided.", status=status.HTTP_400_BAD_REQUEST)
        admin_logger.info(f"Attempted remove admin - admin {request.user.administrator.id}")
        if (adminfacade.remove_administrator(request=request, id=request.query_params['id'])) == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_200_OK)
  

        
        
    