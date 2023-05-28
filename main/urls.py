from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="main",
        default_version='v1',
        description="multi tenant architecture",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[]
)
# swagger_view = schema_view.with_ui('swagger')

jwt_token_security = openapi.SecurityRequirement(
    scheme="Bearer",  # Scheme name for the token (e.g., "Bearer")
    type="http",      # Security type (e.g., "http")
    description="Bearer Token",  # Description for the security requirement
    name="Authorization",        # Header name for the token
    in_=openapi.IN_HEADER,       # Location of the token in the request
)

schema_view.security = [jwt_token_security]
app_name = "tenant"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('tenant.urls')),

    path('api/auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
