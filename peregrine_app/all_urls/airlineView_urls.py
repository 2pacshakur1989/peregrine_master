from django.urls import path
from peregrine_app.all_views import airlineView

app_name = "peregrine_app_airlineView"

urlpatterns = [
    path('airline_generic/',airlineView.airline_generic, name='airline_generic'),
    path('update_airline/', airlineView.update_airline, name='update_airline'),
    path('add_flight/', airlineView.add_flight, name='add_flight'),
    path('get_my_flights/', airlineView.get_my_flights, name='get_my_flights'),
    path('update_flight/<int:flight_id>', airlineView.update_flight, name='update_flight'),
    path('remove_flight/<int:flight_id>', airlineView.remove_flight, name='remove_flight'),
    path('airline_logout_view/', airlineView.logout_view, name='airline_logout_view'),
]