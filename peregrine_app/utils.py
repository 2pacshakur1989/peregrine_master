from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


# def get_token_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return str(refresh.access_token)


# def get_token_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     token = {
#         'access_token': str(refresh.access_token),
#         'user_id': user.id,
#         'username': user.username,
#     }
#     if user.is_staff:
#         token['is_staff'] = True
#     if user.is_superuser:
#         token['is_superuser'] = True
#     if user.groups.filter(name='airline').exists():
#         token['roles'] = ['airline']
#     elif user.groups.filter(name='customer').exists():
#         token['roles'] = ['customer']
#     elif user.groups.filter(name='admin').exists():
#         token['roles'] = ['admin']
#     return token

from rest_framework_simplejwt.tokens import RefreshToken

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    token = {
        'refresh_token': str(refresh),
        'access_token': str(access),
        'user_id': user.id,
        'username': user.username,
    }
    if user.is_staff:
        token['is_staff'] = True
    if user.is_superuser:
        token['is_superuser'] = True
    if user.groups.filter(name='airline').exists():
        token['roles'] = ['airline']
    elif user.groups.filter(name='customer').exists():
        token['roles'] = ['customer']
    elif user.groups.filter(name='admin').exists():
        token['roles'] = ['admin']
    return token


def check_countries(input_country,countries):
    if input_country in countries:
        return True


# def partial_update():

#         if 'username' in request.data:
#             customer.username = request.data['username']
#         if 'email' in request.data:
#             customer.email = request.data['email']
#         if 'password1' in request.data:
#             customer.email = request.data['password1']
#         if 'first_name' in request.data:
#             customer.first_name = request.data['first_name']
#         if 'last_name' in request.data:
#             customer.last_name = request.data['last_name']
#         if 'address' in request.data:
#             customer.address = request.data['address']
#         if 'phone_no' in request.data:
#             customer.phone_no = request.data['phone_no']
#         if 'credit_card_no' in request.data:
#             customer.credit_card_no = request.data['credit_card_no']
#         customer.save()
#         return Response(CustomerSerializer(customer).data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

