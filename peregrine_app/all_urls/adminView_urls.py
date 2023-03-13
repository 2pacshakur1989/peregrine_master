from django.urls import path
from peregrine_app.all_views import adminView

app_name = "peregrine_app_adminView"

urlpatterns = [




    # Get Methods 
    path('admin_generic/',adminView.admin_generic, name='admin_generic'),
    path('get_customers/', adminView.get_customers, name='get_customers'),
    path('get_airlines/', adminView.get_airlines, name='get_airlines'),
    path('get_admins/', adminView.get_admins, name='get_admins'),


    # Post Methods
    path('admin_add_customer/', adminView.admin_add_customer, name='admin_add_customer'),
    path('admin_add_airline/', adminView.admin_add_airline, name='admin_add_airline'),
    path('admin_add_admin/', adminView.admin_add_admin, name='admin_add_admin'),
    path('admin_remove_customer/<int:customer_id>', adminView.admin_remove_customer, name='admin_remove_customer'),
    path('admin_remove_airline/<int:airline_id>', adminView.admin_remove_airline, name='admin_remove_airline'),
    path('admin_remove_admin/<int:admin_id>', adminView.admin_remove_admin, name='admin_remove_admin'),
    path('admin_logout_view/', adminView.logout_view, name='admin_logout_view'),
    
]