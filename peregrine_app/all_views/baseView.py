from django.shortcuts import render,redirect ,HttpResponse
from peregrine_app.facades.facadebase import FacadeBase
from peregrine_app.forms import FlightFilterForm , AirlineFilterForm
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse 
from django.db.models import Q



class Airline:
    facadebase = FacadeBase()

    @classmethod
    def get_all_airlines(cls, request):
        try:
            airlines = cls.facadebase.get_all_airlines()

            if request.method == 'POST':
                form = AirlineFilterForm(request.POST)
                if form.is_valid():  
                    country = form.cleaned_data['country']
                    # filter airlines based on user input
                    if country:
                        airlines = cls.facadebase.get_airline_by_country(country_id=country)
                        return render(request, 'peregrine_app/airlines.html', {'airlines': airlines})

            form = AirlineFilterForm()
            context = {
                'form' : form,
                'airlines' : airlines
            }
            return render(request, 'peregrine_app/airlines.html', context)
        except Exception as e:
            print(f"An error occurred while fetching flights: {e}")
            return HttpResponse ('Oops, Something Went Wrong')



class Flight:
    facadebase = FacadeBase()

    @classmethod
    def get_all_flights(cls, request):
        try:
            all_flights = cls.facadebase.get_all_flights()

            if request.method == 'POST':
                form = FlightFilterForm(request.POST)
                if form.is_valid():
                    origin_country = form.cleaned_data['origin_country']
                    destination_country = form.cleaned_data['destination_country']
                    departure_date = form.cleaned_data['departure_date']
                    landing_date = form.cleaned_data['landing_date']
                    airline_company = form.cleaned_data['airline_company']
                    filtered_flights = all_flights

                    if origin_country:
                        origin_flights = cls.facadebase.get_flights_by_origin_country_id(origin_country_id=origin_country.id)
                        filtered_flights = filtered_flights.filter(id__in=origin_flights.values_list('id', flat=True))

                    if destination_country:
                        destination_flights = cls.facadebase.get_flights_by_destination_country_id(destination_country_id=destination_country.id)
                        filtered_flights = filtered_flights.filter(id__in=destination_flights.values_list('id', flat=True))

                    if departure_date:
                        filtered_flights = filtered_flights.filter(Q(departure_time__date=departure_date))

                    if landing_date:
                        filtered_flights = filtered_flights.filter(Q(landing_time__date=landing_date))

                    if airline_company:
                        airline_flights = cls.facadebase.get_flights_by_airline_company(airline_company_id=airline_company)
                        filtered_flights = filtered_flights.filter(id__in=airline_flights.values_list('id', flat=True))

                    if not filtered_flights.exists():
                        messages.error(request, 'No flights found matching your criteria.')
                        return redirect(reverse('peregrine_app_baseView:get_all_flights'))

                    return render(request, 'peregrine_app/flights.html', {'form': form, 'all_flights': filtered_flights})

            form = FlightFilterForm()
            context = {
                'form': form,
                'all_flights': all_flights,
            }
            return render(request, 'peregrine_app/flights.html', context)

        except Exception as e:
            print(f"An error occurred while fetching flights: {e}")
            return HttpResponse('FUCK')





































































































# class Country:
#     facadebase = FacadeBase()

#     @classmethod
#     def get_all_countries(cls, request):
#         try:
#             countries = cls.facadebase.get_all_countries()
#         except Exception as e:
#             print(f"An error occurred while fetching countries: {e}")
#             return None    
#         return 
    
#     @classmethod
#     def get_country_by_id(cls, request, country_id):
#         try:
#             country = cls.facadebase.get_country_by_id(country_id=country_id)
#         except Exception as e:
#             print(f"An error occurred while fetching country: {e}")
#             return None    
#         return 











# class Flight:
#     facadebase = FacadeBase()

#     @classmethod
#     def get_all_flights(cls, request):
#         try:
#             all_flights = cls.facadebase.get_all_flights()

#             if request.method == 'POST':
#                 form = FlightFilterForm(request.POST)
#                 if form.is_valid():
                    
#                     origin_country = form.cleaned_data['origin_country']
#                     destination_country = form.cleaned_data['destination_country']
#                     departure_date = form.cleaned_data['departure_date']
#                     landing_date = form.cleaned_data['landing_date']
#                     airline_company = form.cleaned_data['airline_company']
#                     # filter flights based on user input
#                     if origin_country:
#                         all_flights = cls.facadebase.get_flights_by_origin_country_id(origin_country_id=origin_country.id)
#                         if not all_flights.exists():
#                             messages.error(request, 'No Flights found, departuring from the selected country ! ')
#                             return redirect(reverse('peregrine_app_baseView:get_all_flights') + '?message=1')
#                         return render(request, 'peregrine_app/flights.html', {'form' : form,'all_flights' : all_flights,})

#                     if destination_country:
#                         all_flights = cls.facadebase.get_flights_by_destination_country_id(destination_country_id=destination_country.id)
#                         if not all_flights.exists():
#                             messages.error(request, 'No Flights found, landing in the selected country ! ')
#                             return redirect(reverse('peregrine_app_baseView:get_all_flights') + '?message=1')
#                         return render(request, 'peregrine_app/flights.html', {'form' : form,'all_flights' : all_flights,})

#                     if departure_date:
#                         all_flights = cls.facadebase.get_flights_by_departure_date(departure_time=departure_date)
#                         return render(request, 'peregrine_app/flights.html', {'all_flights': all_flights})
#                     if landing_date:
#                         all_flights = cls.facadebase.get_flights_by_landing_date(landing_time=landing_date)
#                         return render(request, 'peregrine_app/flights.html', {'all_flights': all_flights})
#                     if airline_company:
#                         all_flights = cls.facadebase.get_flights_by_airline_company(airline_company_id=airline_company)
#                         return render(request, 'peregrine_app/flights.html', {'all_flights': all_flights})
#             form = FlightFilterForm()
#             context = {
#                 'form' : form,
#                 'all_flights' : all_flights,
#             }
#             return render(request, 'peregrine_app/flights.html', context)
#         except Exception as e:
#             print(f"An error occurred while fetching flights: {e}")
#             return HttpResponse ('FUCK')