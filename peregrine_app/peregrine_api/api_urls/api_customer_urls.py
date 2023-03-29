from django.urls import path
from peregrine_app.peregrine_api.api_views import api_customer_views

app_name = "peregrine_app_api_customer_view"

urlpatterns = [

    path('api/customers/', api_customer_views.customer, name='customer'),

]