from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized') 
        return wrapper_func
    return decorator


# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken

# def allowed_users(allowed_roles=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#             # Check if token is present in the request headers
#             try:
#                 raw_token = request.headers['Authorization'].split()[1]
#                 JWTAuthentication().get_validated_token(raw_token)
#                 valid_token = True
#             except (KeyError, InvalidToken):
#                 valid_token = False
            
#             # Check if the user has the required role and a valid token
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#             if group in allowed_roles and valid_token:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponse('You are not authorized') 
#         return wrapper_func
#     return decorator

