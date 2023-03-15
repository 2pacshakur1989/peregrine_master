from django.urls import path
from peregrine_app.all_views import baseView
# from peregrine_app.peregrine_api.api_view import api_views

app_name = "peregrine_app_baseView"


urlpatterns = [

    # Flights urls
    path('get_all_flights/', baseView.Flight.get_all_flights, name='get_all_flights'),

    #Airlines urls
    path('get_all_airlines/', baseView.Airline.get_all_airlines, name='get_all_airlines'),

    # path('api/flights',api_views.flight_list, name='flight_list')

]
