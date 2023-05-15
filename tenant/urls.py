from . import api_views
from django.urls import path

urlpatterns = [
    path('', api_views.AccountCreate.as_view(), name=api_views.AccountCreate.name),
    path('users/', api_views.UserList.as_view(), name=api_views.UserList.name),
    path('users/<uuid:pk>', api_views.UserDetail.as_view(), name=api_views.UserDetail.name),
    path('tenant/', api_views.TenantDetail.as_view(), name=api_views.TenantDetail.name),
]
# router = routers.DefaultRouter()
# router.register('user', UserView.as_view(), basename='user')
# urlpatterns = router.urls
# urlpatterns = [
#     path("user/", UserView.as_view())
# ]
