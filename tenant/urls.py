from django.urls import path

from . import api_views

urlpatterns = [

    # path('api/register/', api_views.UserRegistrationView.as_view(), name='register'),
    path('api/login/', api_views.login, name='login'),
    path('sentry-debug/', api_views.trigger_error),
    path('api/tenant_data/', api_views.TenantData.as_view(), name='tenant_data'),

]
