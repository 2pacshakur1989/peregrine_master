from django.urls import path
# from peregrine_app.all_views import baseView
from peregrine_app.peregrine_api.api_views import api_login_logout_views

app_name = "peregrine_app_api_login_logout_view"


urlpatterns = [

    path('api/login/', api_login_logout_views.LoginView.as_view(), name='login'),
    path('api/logout/',api_login_logout_views.LogoutView.as_view(), name='logout')
]
