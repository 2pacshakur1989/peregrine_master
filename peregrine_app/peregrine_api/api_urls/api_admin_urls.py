from django.urls import path
from peregrine_app.peregrine_api.api_views import api_admin_views

app_name = "peregrine_app_api_admin_view"

urlpatterns = [

    path('api/admins/', api_admin_views.admin, name='admin'),
]