from django.urls import path, include

urlpatterns = [
    path("api/", include("tenant.urls")),
    path("silk/", include("silk.urls", namespace="silk"))
]
