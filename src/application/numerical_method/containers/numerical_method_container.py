from dependency_injector import containers, providers
from src.application.numerical_method.services.bisection_service import BisectionService
from src.application.numerical_method.services.regula_falsi_service import (
    RegulaFalsiService,
)
from src.application.numerical_method.services.fixed_point_service import (
    FixedPointService,
)


class NumericalMethodContainer(containers.DeclarativeContainer):
    bisection_service = providers.Factory(BisectionService)
    regula_falsi_service = providers.Factory(RegulaFalsiService)
    fixed_point_service = providers.Factory(FixedPointService)
