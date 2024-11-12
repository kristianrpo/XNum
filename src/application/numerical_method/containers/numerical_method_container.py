from dependency_injector import containers, providers
from src.application.numerical_method.services.bisection_service import BisectionService
from src.application.numerical_method.services.regula_falsi_service import (
    RegulaFalsiService,
)
from src.application.numerical_method.services.fixed_point_service import (
    FixedPointService,
)
from src.application.numerical_method.services.jacobi_service import JacobiService

from src.application.numerical_method.services.gauss_seidel_service import (
    GaussSeidelService,
)
from src.application.numerical_method.services.sor_service import (
    SORService,
)
from src.application.numerical_method.services.vandermonde_service import (
    VandermondeService,
)


class NumericalMethodContainer(containers.DeclarativeContainer):
    bisection_service = providers.Factory(BisectionService)
    regula_falsi_service = providers.Factory(RegulaFalsiService)
    fixed_point_service = providers.Factory(FixedPointService)
    jacobi_service = providers.Factory(JacobiService)
    gauss_seidel_service = providers.Factory(GaussSeidelService)
    sor_service = providers.Factory(SORService)
    vandermonde_service = providers.Factory(VandermondeService)
