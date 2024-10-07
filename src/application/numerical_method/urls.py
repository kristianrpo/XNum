from django.urls import path
from . import views as numerical_method

app_name = "numerical_method"
urlpatterns = [
    path(
        "bisection/",
        numerical_method.BisectionView.as_view(),
        name="bisection",
    ),
]
