from django.urls import path
from peregrine_app.peregrine_api.api_views import api_flight_views

app_name = "peregrine_app_api_flight_view"


urlpatterns = [

    # GET URLS
    path('api/flights/',api_flight_views.flight, name='flight'),
    path('api/flights/<str:id>', api_flight_views.flight, name='flight'),
    path('api/flights/<str:origin>',api_flight_views.flight, name='flight'),
    path('api/flights/<str:destination>',api_flight_views.flight, name='flight'),
    path('api/flights/<str:airline>',api_flight_views.flight, name='flight'),
    path('api/flights/<str:departure>',api_flight_views.flight, name='flight'),
    path('api/flights/<str:landing>',api_flight_views.flight, name='flight'),

]





