from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from peregrine_app.facades.anonymousfacade import AnonymousFacade

facade = AnonymousFacade()

class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = facade.token_dal.create_token(user=user)
            # Include additional information in the token payload
            token_payload = {
                'user_id': user.id,
                'username': user.username,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
            if user.groups.filter(name='airline').exists():
                token_payload['roles'] = ['airline']
            elif user.groups.filter(name='customer').exists():
                token_payload['roles'] = ['customer']
            elif user.groups.filter(name='admin').exists():
                token_payload['roles'] = ['admin']
            return Response({'token': token.key, 'payload': token_payload})
        else:
            return Response({'error': 'Invalid credentials'})
        

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            facade.token_dal.delete_token(user=request.user)
            # Token.objects.filter(user=request.user).delete()
        except Token.DoesNotExist:
            pass
        return Response({'success': 'Successfully logged out.'})