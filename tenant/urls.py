from django.urls import path

from . import api_views

urlpatterns = [

    path('api/register/', api_views.UserRegistrationView.as_view(), name='register'),
    path('api/login/', api_views.login, name='login'),
]
