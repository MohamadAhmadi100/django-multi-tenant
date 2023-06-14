from django.urls import path

from . import api_views

urlpatterns = [

    # path('api/register/', api_views.UserRegistrationView.as_view(), name='register'),
    path('login/', api_views.login, name='login'),
    path('sentry-debug/', api_views.trigger_error),
    path('tenant_data/', api_views.TenantData.as_view(), name='tenant_data'),
    path('get-configs/', api_views.ConfigView.as_view(), name='config'),
    path('refresh-configs/', api_views.RefreshConsulConfigView.as_view(), name='refresh_configs'),
]
