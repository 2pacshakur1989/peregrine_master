from django.urls import path
from peregrine_app.peregrine_api.api_views import api_ticket_views

app_name = "peregrine_app_api_ticket_view"

urlpatterns = [

    path('api/tickets/', api_ticket_views.ticket, name='ticket'),
]
