from dependency_injector import containers, providers
from src.application.numerical_method.services.bisection_service import BisectionService


class NumericalMethodContainer(containers.DeclarativeContainer):
    bisection_service = providers.Factory(BisectionService)
