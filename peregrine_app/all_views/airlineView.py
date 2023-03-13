from django.shortcuts import render,redirect ,HttpResponse
from django.contrib.auth.decorators import login_required 
from peregrine_app.forms import  UpdateAirlineForm , UpdateUserForm, AddFlightForm, UpdateFlightForm
from peregrine_app.facades.airlinefacade import AirlineFacade
from django.db import transaction
from django.http import HttpResponseServerError
from peregrine_app.decorators import allowed_users 
from django.contrib.auth import logout


facade = AirlineFacade()

@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['airline'])
def airline_generic(request):
        
        return render(request, 'peregrine_app/airline.html')


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['airline'])
def update_airline(request):

    airline_company = request.user.airlinecompany
    user = request.user
    airline_form = UpdateAirlineForm(instance=airline_company)
    user_form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        airline_form = UpdateAirlineForm(request.POST, instance=airline_company)
        user_form = UpdateUserForm(request.POST, instance=user)
        if airline_form.is_valid() and user_form.is_valid():
            try:
                with transaction.atomic():
                    facade.update_airline(id=airline_company.id, data=airline_form.cleaned_data)
                    facade.update_user(id=user.id,data=user_form.cleaned_data)
                    return redirect('peregrine_app_airlineView:airline_generic')
            except Exception as e:
                # rollback the update
                transaction.set_rollback(True)
                # handle the exception 
                return HttpResponseServerError('Failed to update customer and user data: {}'.format(str(e)))
    context = {
         'customer_form': airline_form,
         'user_form': user_form
    }
    return render(request, 'peregrine_app/updateairline.html', context)


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['airline'])
def get_my_flights(request):
        
        airline_company = request.user.airlinecompany
        try:
            my_flights = facade.get_my_flights(airline_company_id=airline_company)
            return render(request, 'peregrine_app/airline_all_flights.html' , {'my_flights':my_flights})
        except Exception as e:
            print(f"An error occurred while fetching flights: {e}")
            return HttpResponse('Oops, Something Went Wrong')


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['airline'])
def add_flight(request):

    airline_company = request.user.airlinecompany
    form = AddFlightForm()
    if request.method == 'POST':
        form = AddFlightForm(request.POST)
        if form.is_valid():
            try:
                flight_data = {
                    'airline_company_id': airline_company,
                    'origin_country_id': form.cleaned_data['origin_country_id'],
                    'destination_country_id': form.cleaned_data['destination_country_id'],
                    'departure_time': form.cleaned_data['departure_time'],
                    'landing_time': form.cleaned_data['landing_time'],
                    'remaining_tickets': form.cleaned_data['remaining_tickets'],
                }
                facade.add_flight(data=flight_data)
                return redirect('peregrine_app_airlineView:airline_generic')
            except Exception as e:
                print(f"An error occurred while adding a flight: {e}")
                return HttpResponse ('Oops, Something Went Wrong')
    else:
        form = AddFlightForm()
        context = {
            'form' : form,
        }
        return render(request, 'peregrine_app/addflight.html', context)
    context = {
        'form': form,
        'form_errors': form.errors if 'user_form' in locals() else None,
    }
    return render(request, 'peregrine_app/addflight.html', context)


@login_required(login_url='peregrine_app_anonymousView:login_view')
@allowed_users(allowed_roles=('airline'))
def update_flight(request, flight_id):

    flight = facade.get_flight_by_id(id=flight_id)
    flight_form = UpdateFlightForm(instance=flight)
    if request.method == 'POST':
        flight_form = UpdateFlightForm(request.POST , instance=flight)
        if flight_form.is_valid():
            try:
                facade.update_flight(flight_id=flight_id, data=flight_form.cleaned_data)
                return redirect('peregrine_app_airlineView:get_my_flights')
            except Exception as e:
                # handle the exception 
                return HttpResponseServerError('Failed to update flight: {}'.format(str(e)))
    context = {
        'flight_form': flight_form,
        'flight_form_errors': flight_form.errors if 'user_form' in locals() else None,
    }
    return render(request, 'peregrine_app/updateflight.html', context)


@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=('airline'))
def remove_flight(request, flight_id):

    try:
        facade.remove_flight(flight_id=flight_id)
        return redirect('peregrine_app_airlineView:get_my_flights')
    except Exception as e:
        return HttpResponseServerError('Failed to remove flight: {}'.format(str(e)))
    

@login_required(login_url='peregrine_app_anonymousView:landing_page')
@allowed_users(allowed_roles=['airline'])
def logout_view(request):
    logout(request)
    return redirect('peregrine_app_anonymousView:landing_page')
