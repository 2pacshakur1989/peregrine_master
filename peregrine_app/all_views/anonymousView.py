from django.shortcuts import render,redirect ,HttpResponse ,HttpResponseRedirect
from django.http import JsonResponse
from peregrine_app.forms import UserProfile , AddCustomerForm
from peregrine_app.facades.anonymousfacade import AnonymousFacade,AdministratorFacade,AirlineFacade,CustomerFacade
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from django.urls import reverse 
from peregrine_app.forms import LoginForm
from peregrine_app.exceptions import UserNotFoundError
from django.views.generic.edit import FormView
from peregrine_app.decorators import allowed_users
import json
from rest_framework.authtoken.models import Token
from peregrine_app.utils import get_token_for_user
from rest_framework_simplejwt.tokens import RefreshToken


facade = AnonymousFacade()
    
def landing_page(request):
    
    form = LoginForm()
    return render(request, 'peregrine_app/landing_page.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             try:
#                 username = form.cleaned_data['username']
#                 password = form.cleaned_data['password']
#                 user = authenticate(request, username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     right_facade = facade.get_facade_for_user(user=user)
#                     if isinstance(right_facade, AdministratorFacade):
#                         return redirect(('peregrine_app_adminView:admin_generic'))
#                     elif isinstance(right_facade, AirlineFacade):
#                         return redirect(reverse('peregrine_app_airlineView:airline_generic'))
#                     elif isinstance(right_facade, CustomerFacade):
#                         return redirect(reverse('peregrine_app_customerView:customer_generic'))
#             except Exception as e:
#                 print(f"An error occurred while logging in: {e}")
#                 return None
#     else:
#         form = LoginForm()
#         return render(request, 'peregrine_app/landing_page.html', {'form': form})
#     context = {
#         'form': form,
#         'form_errors': form.errors if 'user_form' in locals() else None,
#         'login_error': 'Invalid username or password. Please try again.',
#     }
#     return render(request, 'peregrine_app/landing_page.html', context)


def add_customer(request):

    if request.method == 'POST':
        user_form = UserProfile(request.POST)
        customer_form = AddCustomerForm(request.POST)
        if (user_form.is_valid()) and (customer_form.is_valid()):
            try:
                facade.add_customer(user_data=user_form.cleaned_data,data=customer_form.cleaned_data)
                return redirect('peregrine_app_anonymousView:login_view')
            except Exception as e:
                print(f"An error occurred while adding a customer: {e}")
                return HttpResponse ("Oops, Something Went Wrong!")
    else:
        user_form = UserProfile()
        customer_form = AddCustomerForm()
        context = {
            'user_form' : user_form,
            'customer_form' : customer_form,
        }
        return render(request, 'peregrine_app/signup.html', context)
    context = {
        'user_form': user_form,
        'customer_form': customer_form,
        'user_form_errors': user_form.errors if 'user_form' in locals() else None,
        'customer_form_errors': customer_form.errors if 'customer_form' in locals() else None,
    }
    return render(request, 'peregrine_app/signup.html', context)



def login_view(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    token = get_token_for_user(user=user)
                    right_facade = facade.get_facade_for_user(user=user,token=token)
                    if isinstance(right_facade, AdministratorFacade):
                        redirect_url = 'peregrine_app_adminView:admin_generic'
                    elif isinstance(right_facade, AirlineFacade):
                        redirect_url = 'peregrine_app_airlineView:airline_generic'
                    elif isinstance(right_facade, CustomerFacade):
                        redirect_url = 'peregrine_app_customerView:customer_generic'
                    else:
                        raise ValueError("Invalid user type")
                    # response.set_cookie('token', token['access_token'], httponly=True)
                    response = redirect(reverse(redirect_url))
                    # response.set_cookie('token', token['access_token'], httponly=True)
                    response['token'] = token
                    print(f"Token generated: {token}")
                    return response
            except Exception as e:
                print(f"An error occurred while logging in: {e}")
    else:
        form = LoginForm()
    context = {
        'form': form,
        'form_errors': form.errors if 'user_form' in locals() else None,
        'login_error': 'Invalid username or password. Please try again.',
    }
    return render(request, 'peregrine_app/landing_page.html', context)



