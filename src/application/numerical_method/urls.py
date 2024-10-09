from django.urls import path
from .views.bisection_view import BisectionView
from .views.regula_falsi_view import RegulaFalsiView

app_name = "numerical_method"
urlpatterns = [
    path(
        "bisection/",
        BisectionView.as_view(),
        name="bisection",
    ),
    path(
        "regula-falsi/",
        RegulaFalsiView.as_view(),
        name="regula_falsi",
    ),
]
