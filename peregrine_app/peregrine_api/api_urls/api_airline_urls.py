from django.urls import path
from peregrine_app.peregrine_api.api_views import api_airline_views

app_name = "peregrine_app_api_airline_view"

urlpatterns = [

    # GET URLS
    path('api/airlines/', api_airline_views.airline, name='airline'),
    # path('api/airlines/<str:country_id>', api_airline_views.airline, name='airline'),

    # # POST/PATCH/DELETE URLS
    path('api/airlines/<str:id>', api_airline_views.airline, name='airline')
]