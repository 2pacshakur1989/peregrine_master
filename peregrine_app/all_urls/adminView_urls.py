from django.urls import path
from peregrine_app.all_views import adminView

app_name = "peregrine_app_adminView"

urlpatterns = [
    path('admin_generic/',adminView.admin_generic, name='admin_generic'),
    path('admin_logout_view/', adminView.logout_view, name='admin_logout_view'),
    path('user_choice/', adminView.user_choice, name='user_choice'),
    path('admin_add_customer/', adminView.admin_add_customer, name='admin_add_customer'),
    path('admin_add_airline/', adminView.admin_add_airline, name='admin_add_airline'),
    path('admin_add_admin/', adminView.admin_add_admin, name='admin_add_admin'),
    path('admin_remove_customer/<int:customer_id>', adminView.admin_remove_customer, name='admin_remove_customer'),
    path('admin_remove_airline/<int:airline_id>', adminView.admin_remove_airline, name='admin_remove_airline'),
    path('admin_remove_admin/<int:admin_id>', adminView.admin_remove_admin, name='admin_remove_admin'),
]