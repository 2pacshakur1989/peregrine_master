"""peregrine_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [


    # API urls
    path('', include("peregrine_app.peregrine_api.api_urls.api_flight_urls", namespace='peregrine_app_api_flight_view')),
    path('', include("peregrine_app.peregrine_api.api_urls.api_login-logout_urls", namespace='peregrine_app_login_logout_api_view')),
    path('', include("peregrine_app.peregrine_api.api_urls.api_customer_urls", namespace='peregrine_app_api_customer_view')),
    path('', include("peregrine_app.peregrine_api.api_urls.api_airline_urls", namespace='peregrine_app_api_airline_view')),
    path('', include("peregrine_app.peregrine_api.api_urls.api_ticket_urls", namespace='peregrine_app_api_ticket_view')),
    path('', include("peregrine_app.peregrine_api.api_urls.api_country_urls", namespace='peregrine_app_api_country_view')),
    path('', include("peregrine_app.peregrine_api.api_urls.api_admin_urls", namespace='peregrine_app_api_admin_view')),


    path('admin/', admin.site.urls),

]





