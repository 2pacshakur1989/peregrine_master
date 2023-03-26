"""Login/Logout API View"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from peregrine_app.facades.anonymousfacade import AnonymousFacade

anonymousfacade = AnonymousFacade()

        
class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        return Response (anonymousfacade.login_func(request=request ,username=username, password=password))    

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        return Response (anonymousfacade.logout_func(request,user))
        