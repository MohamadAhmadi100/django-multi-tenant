from django.urls import path, include

urlpatterns = [
    path("api/", include("tenant.urls")),
    path("api/silk/", include("silk.urls", namespace="silk"))
]
