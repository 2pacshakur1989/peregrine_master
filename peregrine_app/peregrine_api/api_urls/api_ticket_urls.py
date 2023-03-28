from django.urls import path
from peregrine_app.peregrine_api.api_views import api_ticket_views

app_name = "peregrine_app_api_ticket_view"

urlpatterns = [

    path('api/tickets/', api_ticket_views.ticket, name='ticket'),
    path('api/tickets/<str:flight_id>', api_ticket_views.ticket, name='ticket'),
    # path('api/tickets/<str:ticket_id>', api_ticket_views.ticket, name='ticket')
]
