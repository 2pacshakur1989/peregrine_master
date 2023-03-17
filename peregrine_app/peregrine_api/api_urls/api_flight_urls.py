from django.urls import path
# from peregrine_app.all_views import baseView
from peregrine_app.peregrine_api.api_views import api_flight_views

app_name = "peregrine_app_api_flight_view"


urlpatterns = [

    # GET URLS
    path('api/flights/',api_flight_views.flight, name='flight'),
    path('api/flights/origin/<str:origin>',api_flight_views.flight, name='flight'),
    path('api/flights/destination/<str:destination>',api_flight_views.flight, name='flight'),
    path('api/flights/airline/<str:airline>',api_flight_views.flight, name='flight'),
    path('api/flights/departure/<str:departure>',api_flight_views.flight, name='flight'),
    path('api/flights/landing/<str:landing>',api_flight_views.flight, name='flight'),


    # POST URLS
    path('api/flights/addflight/', api_flight_views.flight, name='flight'),


    # PUT URLS
    path('api/flights/updateflight/<str:id>',api_flight_views.flight, name='flight'),

    # DELETE URLS
    path('api/flights/deleteflight/<str:id>',api_flight_views.flight, name='flight_lst')

]





