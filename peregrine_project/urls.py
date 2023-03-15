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

    # App urls
    path('', include("peregrine_app.all_urls.baseView_urls", namespace='peregrine_app_baseView')),
    path('', include("peregrine_app.all_urls.anonymousView_urls", namespace='peregrine_app_anonymousView')),
    path('', include("peregrine_app.all_urls.adminView_urls", namespace='peregrine_app_adminView')),
    path('', include("peregrine_app.all_urls.airlineView_urls", namespace='peregrine_app_airlineView')),
    path('', include("peregrine_app.all_urls.customerView_urls", namespace='peregrine_app_customerView')),

    # API urls
    path('', include("peregrine_app.peregrine_api.api_urls.api_flight_urls", namespace='peregrine_app_api_flight_view')),
    path('', include("peregrine_app.peregrine_api.api_urls.api_login-logout_urls", namespace='peregrine_app_login_logout_api_view')),

    path('admin/', admin.site.urls),

]





