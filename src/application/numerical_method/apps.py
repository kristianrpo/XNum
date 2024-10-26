from django.apps import AppConfig
from .containers.numerical_method_container import NumericalMethodContainer


class NumericalMethodConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.application.numerical_method"

    def ready(self) -> None:
        container = NumericalMethodContainer()
        container.wire(
            modules=[
                "src.application.numerical_method.views.bisection_view",
                "src.application.numerical_method.views.regula_falsi_view",
                "src.application.numerical_method.views.fixed_point_view",
                "src.application.numerical_method.views.fixed_point_view",
            ]
        )
