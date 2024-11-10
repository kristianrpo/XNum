from django.urls import path
from .views.bisection_view import BisectionView
from .views.regula_falsi_view import RegulaFalsiView
from .views.fixed_point_view import FixedPointView
from .views.jacobi_view import JacobiView
from .views.gauss_seidel_view import GaussSeidelView
from .views.sor_view import SORView

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
    path(
        "fixed-point/",
        FixedPointView.as_view(),
        name="fixed_point",
    ),
    path(
        "jacobi/",
        JacobiView.as_view(),
        name="jacobi",
    ),
    path(
        "gauss-seidel/",
        GaussSeidelView.as_view(),
        name="gauss_seidel",
    ),
    path(
        "sor/",
        SORView.as_view(),
        name="sor",
    )
]
