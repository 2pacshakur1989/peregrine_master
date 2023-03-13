from django.urls import path
from peregrine_app.all_views import anonymousView

app_name = "peregrine_app_anonymousView"

urlpatterns = [
    path('',anonymousView.landing_page, name='landing_page'),
    path('add_customer/', anonymousView.add_customer, name='add_customer'),
    path('login_view/', anonymousView.login_view, name='login_view'),
]