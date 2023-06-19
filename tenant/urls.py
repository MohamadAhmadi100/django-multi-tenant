from django.urls import path

from . import api_views

urlpatterns = [
    path('user/list', api_views.ListUsersView.as_view(), name='list-users'),
    path('user/get', api_views.RetrieveUserView.as_view(), name='get-user'),
    path('organization/get', api_views.RetrieveOrganizationView.as_view(), name='get-organization'),
    path('organization/list', api_views.ListOrganizationsView.as_view(), name='list-organizations'),
    path('sentry-debug', api_views.trigger_error),
    path('config/get', api_views.ConfigView.as_view(), name='get-config'),
    path('config/refresh', api_views.RefreshConsulConfigView.as_view(), name='refresh-configs'),
]
