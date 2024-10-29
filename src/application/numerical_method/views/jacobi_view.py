from django.views.generic import TemplateView
from src.application.numerical_method.interfaces.matrix_method import MatrixMethod
from src.application.numerical_method.containers.numerical_method_container import (
    NumericalMethodContainer,
)
from dependency_injector.wiring import inject
from django.http import HttpRequest, HttpResponse

class JacobiView(TemplateView):
    template_name = "jacobi.html"

    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.method_service = NumericalMethodContainer.jacobi_service()

    def post(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        context = self.get_context_data()

        try:
            # Validación y conversión de la matriz A
            matrix_a_raw = request.POST.get("matrix_a", "")
            A = [
                [float(num) for num in row.strip().split()]
                for row in matrix_a_raw.split(';') if row.strip()
            ]

            # Validación y conversión del vector b
            vector_b_raw = request.POST.get("vector_b", "")
            b = [float(num) for num in vector_b_raw.strip().split()]

            # Validación y conversión del vector inicial x0
            initial_guess_raw = request.POST.get("initial_guess", "")
            x0 = [float(num) for num in initial_guess_raw.strip().split()]

            # Validación y conversión de tolerancia y número máximo de iteraciones
            tolerance = float(request.POST.get("tolerance", 0))
            max_iterations = int(request.POST.get("max_iterations", 100))

        except ValueError:
            # Si hay un error en la conversión, devolvemos un mensaje de error genérico
            context["template_data"] = {
                "message_method": "Error: Todas las entradas deben ser numéricas.",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "solution": [],
            }
            return self.render_to_response(context)

        # Ejecutar el método Jacobi con los parámetros recibidos
        method_response = self.method_service.solve(
            A=A,
            b=b,
            x0=x0,
            tolerance=tolerance,
            max_iterations=max_iterations,
        )

        # Si el servicio retorna un error de validación, mostrarlo en la página
        if not method_response["is_successful"]:
            context["template_data"] = method_response
            return self.render_to_response(context)

        # Verificación de éxito y almacenamiento de la respuesta
        context["template_data"] = method_response
        context["indices"] = list(range(1, len(A) + 1))

        return self.render_to_response(context)
