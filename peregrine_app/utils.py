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


