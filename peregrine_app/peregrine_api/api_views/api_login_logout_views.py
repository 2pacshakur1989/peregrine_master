"""Login/Logout API View"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from peregrine_app.facades.anonymousfacade import AnonymousFacade
from rest_framework.exceptions import AuthenticationFailed
from peregrine_app.loggers import loginout_logger

anonymousfacade = AnonymousFacade()

        
class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        if request.user.is_authenticated:
            # If user is already authenticated, return an error response
            loginout_logger.info(f"User is already logged in")
            raise AuthenticationFailed('User is already logged in')
        username = request.data.get('username')
        password = request.data.get('password')
        loginout_logger.info(f"User attempted login")
        return Response (anonymousfacade.login_func(request=request ,username=username, password=password))    

class LogoutView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        loginout_logger.info(f"User logged out sucessfully")
        return Response (anonymousfacade.logout_func(request=request,user=user))
        