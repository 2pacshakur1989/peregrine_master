from django.urls import path
from peregrine_app.peregrine_api.api_views import api_country_views

app_name = "peregrine_app_api_country_view"

urlpatterns = [

    path('api/countries/', api_country_views.country, name='country'),
]