from django.urls import path
from peregrine_app.peregrine_api.api_views import api_flight_views

app_name = "peregrine_app_api_flight_view"


urlpatterns = [

    path('api/flights/',api_flight_views.flight, name='flight'),
]





