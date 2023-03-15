from django.shortcuts import render,redirect ,HttpResponse
from peregrine_app.forms import UpdateCustomerForm , UpdateUserForm
from peregrine_app.facades.customerfacade import CustomerFacade
from peregrine_app.decorators import allowed_users 
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseServerError
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse 
from django.core import signing
from django.contrib import messages

facade = CustomerFacade()

@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['customer'])
def customer_generic(request):
        return render(request, 'peregrine_app/customer.html')


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['customer'])
def add_ticket(request,flight_id):

    flight = facade.get_flight_by_id(id=flight_id)
    customer = request.user.customer
    try:
        
        ticket_data = {
                    'flight_id': flight,
                    'customer_id': customer}
        new_ticket = facade.add_ticket(data=ticket_data)
        if new_ticket == False:
            messages.error(request, 'Customer cannot add the same ticket twice.')
            return redirect(reverse('peregrine_app_baseView:get_all_flights'))
        if new_ticket == None:
            pass
        
        return render(request, 'peregrine_app/customer.html')
    except Exception as e:
        print(f"An error occurred while adding ticket: {e}")
        return HttpResponse ('Oops, Something Went Wrong')    


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['customer'])
def get_my_tickets(request):
     
    customer = request.user.customer
    try:
        my_tickets = facade.get_my_tickets(customer_id=customer.id)
        return render(request, 'peregrine_app/customer_mytickets.html', {'my_tickets' : my_tickets})
    except Exception as e:
        print(f"An error occurred while fetching tickets: {e}")
        return HttpResponse ('Oops, Something Went Wrong')      


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['customer'])
def remove_ticket(request, ticket_id):
    
    try:
        facade.remove_ticket(id=ticket_id)
        return redirect('peregrine_app_customerView:get_my_tickets')
    except Exception as e:
        return HttpResponseServerError('Failed to remove ticket: {}'.format(str(e)))


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['customer'])
def update_customer(request):
    customer = request.user.customer
    user = request.user
    customer_form = UpdateCustomerForm(instance=customer)
    user_form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        customer_form = UpdateCustomerForm(request.POST, instance=customer)
        user_form = UpdateUserForm(request.POST, instance=user)
        if customer_form.is_valid() and user_form.is_valid():
            try:
                with transaction.atomic():
                    facade.update_customer(customer_id=customer.id, data=customer_form.cleaned_data)
                    facade.update_user(id=user.id,data=user_form.cleaned_data)
                    messages.success(request, 'Updated successfully')
                    return redirect('peregrine_app_customerView:customer_generic')
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                # handle the exception (e.g. log the error message, return an error response)
                return HttpResponseServerError('Failed to update customer and user data: {}'.format(str(e)))
    context = {
         'customer_form': customer_form,
         'user_form': user_form
    }
    return render(request, 'peregrine_app/updatecustomer.html', context)


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['customer'])
def logout_view(request):

    logout(request)
    return redirect('peregrine_app_anonymousView:landing_page')





# @login_required(login_url='peregrine_app_anonymousView:landing_page')
# @allowed_users(allowed_roles=['customer'])
# def logout_view(request):
#     # Extract token from cookie
#     token = request.COOKIES.get('token')
#     print(token)

#     # Blacklist token if it exists
#     if token is not None:
#         print(f"Token terminated: {token}")
#         token_obj = RefreshToken(signing.loads(token))
#         token_obj.blacklist()
#     # Logout the user
#     logout(request)

#     # Remove the token cookie
#     response = redirect('peregrine_app_anonymousView:landing_page')
#     response.delete_cookie('token')
#     return response


