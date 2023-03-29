from django.urls import path
from peregrine_app.peregrine_api.api_views import api_airline_views

app_name = "peregrine_app_api_airline_view"

urlpatterns = [

    path('api/airlines/', api_airline_views.airline, name='airline'),
]