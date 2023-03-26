from peregrine_app.facades.adminfacade import AdministratorFacade
from django.shortcuts import render,redirect ,HttpResponse
from django.http import HttpResponseServerError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 
from peregrine_app.decorators import allowed_users 
from peregrine_app.forms import UserProfile , AddCustomerForm, UserFilterForm, AddAirlineForm, AddAdminForm
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth ,messages
from django.urls import reverse , reverse_lazy
from django.views import View
from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
        
facade = AdministratorFacade(user_group='admin')


# Get Methods
@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def admin_generic(request):
        
        form = UserFilterForm()
        return render(request, 'peregrine_app/admin.html',{'form' : form})
        
@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def get_customers(request):
    customers = facade.get_all_customers()
    return render(request, 'peregrine_app/admin_customers.html', {'customers' : customers})

@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def get_airlines(request):
    airlines = facade.get_all_airlines()
    return render(request, 'peregrine_app/admin_airlines.html', {'airlines' : airlines})

@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def get_admins(request):
    admins = facade.get_all_admins()
    return render(request, 'peregrine_app/admin_admins.html', {'admins' : admins})





# Post methods
@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def admin_add_customer(request):

    if request.method == 'POST':
        user_form = UserProfile(request.POST)
        customer_form = AddCustomerForm(request.POST)
        if (user_form.is_valid()) and (customer_form.is_valid()):
            try:
                facade.add_customer(user_data=user_form.cleaned_data,data=customer_form.cleaned_data)
                return redirect(reverse('peregrine_app_adminView:get_customers'))
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
                                   

@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def admin_add_airline(request):

    if request.method == 'POST':
        user_form = UserProfile(request.POST)
        airline_form = AddAirlineForm(request.POST)
        if (user_form.is_valid()) and (airline_form.is_valid()):
            try:
                facade.add_airline(user_data=user_form.cleaned_data,data=airline_form.cleaned_data)
                return redirect('peregrine_app_adminView:get_airlines')
            except Exception as e:
                print(f"An error occurred while adding airline: {e}")
                return HttpResponse ("Oops, Something Went Wrong!")
    else:
        user_form = UserProfile()
        airline_form = AddAirlineForm()
        context = {
            'user_form': user_form,
            'airline_form': airline_form
        }
        return render(request, 'peregrine_app/admin_add_airline.html', context)
    context = {
        'user_form': user_form,
        'airline_form': airline_form,
        'user_form_errors': user_form.errors if 'user_form' in locals() else None,
        'airline_form_errors': airline_form.errors if 'airline_form' in locals() else None,
    }
    return render(request, 'peregrine_app/admin_add_airline.html', context)
      

@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def admin_add_admin(request):

    if request.method == 'POST':
        user_form = UserProfile(request.POST)
        admin_form = AddAdminForm(request.POST)
        if (user_form.is_valid()) and (admin_form.is_valid()):
            try:
                facade.add_administrator(user_data=user_form.cleaned_data,data=admin_form.cleaned_data)
                return redirect('peregrine_app_adminView:user_choice')
            except Exception as e:
                print(f"An error occurred while adding admin: {e}")
                return HttpResponse ("Oops, Something Went Wrong!")
    else:
        user_form = UserProfile()
        admin_form = AddAdminForm()
        context = {
            'user_form': user_form,
            'admin_form': admin_form
        }
        return render(request, 'peregrine_app/admin_add_admin.html', context)
    context = {
        'user_form': user_form,
        'admin_form': admin_form,
        'user_form_errors': user_form.errors if 'user_form' in locals() else None,
        'admin_form_errors': admin_form.errors if 'admin_form' in locals() else None,
    }
    return render(request, 'peregrine_app/admin_add_admin.html', context)


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def admin_remove_customer(request,customer_id):

    try:
        remove = facade.remove_customer(customer_id=customer_id)
        if remove == True:
            return redirect('peregrine_app_adminView:get_customers')
        else:
            error = 'Note ! The selected Customer has on going active/purchased ticket/s, thus cannot be remove !'
            customers = facade.get_all_customers()
            context = {
                'customers' : customers,
                'error' : error
            }
            return render(request, 'peregrine_app/admin_customers.html', context)
      
    except Exception as e:
        return HttpResponseServerError('Failed to remove customer: {}'.format(str(e)))


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def admin_remove_airline(request,airline_id):

    try:
        remove = facade.remove_airline(id=airline_id)
        if remove == True:
            return redirect('peregrine_app_adminView:get_airlines')
        else:                
            error = """Note ! The selected Airline has an on going active flight/s,
              which has purchased tickets, thus cannot be removed !"""
            airlines = facade.get_all_airlines()
            context = {
                'airlines' : airlines,
                'error' : error
            }
            return render(request, 'peregrine_app/admin_airlines.html', context)
    except Exception as e:
        return HttpResponseServerError('Failed to remove airline: {}'.format(str(e)))


# Add conditions for superuser (admin cannot delete superusers)
@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def admin_remove_admin(request,admin_id):

    try:
        facade.remove_administrator(id=admin_id)
        return redirect('peregrine_app_adminView:user_choice')
    except Exception as e:
        return HttpResponseServerError('Failed to remove admin: {}'.format(str(e)))
    


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['admin'])
def logout_view(request):

    logout(request)
    return redirect('peregrine_app_anonymousView:landing_page')
