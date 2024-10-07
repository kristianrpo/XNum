from django.urls import path
from .views.bisection_view import BisectionView

app_name = "numerical_method"
urlpatterns = [
    path(
        "bisection/",
        BisectionView.as_view(),
        name="bisection",
    ),
]
