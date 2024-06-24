from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("banks/", include("banks.urls")),
    path("api/v1/banks/", include("banks.urls")),
]
