from django.urls import path, include

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include("src.application.home.urls")),
    path("numerical-methods/", include("src.application.numerical_method.urls")),
]
