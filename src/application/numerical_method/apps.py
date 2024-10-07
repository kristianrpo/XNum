# apps.py
from django.apps import AppConfig
from .containers.numerical_method_container import NumericalMethodContainer

class NumericalMethodConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.application.numerical_method"

    def ready(self):
        container = NumericalMethodContainer()
        container.wire(modules=["src.application.numerical_method.views"])
