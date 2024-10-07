from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include("applications.home.urls")),
    path("numerical-methods/", include("applications.numerical_method.urls")),
]
