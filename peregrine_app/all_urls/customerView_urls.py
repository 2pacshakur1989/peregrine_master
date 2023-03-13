from django.urls import path
from peregrine_app.all_views import customerView

app_name = "peregrine_app_customerView"

urlpatterns = [
    path('customer_generic/',customerView.customer_generic, name='customer_generic'),
    path('update_customer/',customerView.update_customer, name='update_customer'),
    path('customer_logout_view/', customerView.logout_view, name='customer_logout_view'),
    path('add_ticket/<int:flight_id>', customerView.add_ticket, name='add_ticket'),
    path('get_my_tickets/', customerView.get_my_tickets, name='get_my_tickets'),
    path('remove_ticket/<int:ticket_id>', customerView.remove_ticket, name='remove_ticket')
]