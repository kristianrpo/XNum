from django.views.generic import TemplateView
from src.application.numerical_method.interfaces.matrix_method import MatrixMethod
from src.application.numerical_method.containers.numerical_method_container import (
    NumericalMethodContainer,
)
from dependency_injector.wiring import inject
from django.http import HttpRequest, HttpResponse

class GaussSeidelView(TemplateView):
    template_name = "gauss_seidel.html"

    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.method_service = NumericalMethodContainer.gauss_seidel_service()

    def post(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        context = self.get_context_data()

        try:
            # Capturar el tamaño de la matriz
            matrix_size = int(request.POST.get("matrix_size", 3))

            # Validación y conversión de la matriz A
            matrix_a_raw = request.POST.get("matrix_a", "")
            A = [
                [float(num) for num in row.strip().split()]
                for row in matrix_a_raw.split(';') if row.strip()
            ]

            # Validar que A tiene el tamaño correcto
            if len(A) != matrix_size or any(len(row) != matrix_size for row in A):
                raise ValueError("La matriz A no tiene el tamaño seleccionado.")

            # Validación y conversión del vector b
            vector_b_raw = request.POST.get("vector_b", "")
            b = [float(num) for num in vector_b_raw.strip().split()]
            if len(b) != matrix_size:
                raise ValueError("El vector b no tiene el tamaño seleccionado.")

            # Validación y conversión del vector inicial x0
            initial_guess_raw = request.POST.get("initial_guess", "")
            x0 = [float(num) for num in initial_guess_raw.strip().split()]
            if len(x0) != matrix_size:
                raise ValueError("El vector inicial x0 no tiene el tamaño seleccionado.")

            # Validación y conversión de tolerancia y número máximo de iteraciones
            tolerance = float(request.POST.get("tolerance", 0))
            max_iterations = int(request.POST.get("max_iterations", 100))

            # Validar el tipo y el valor de precisión
            precision_type = request.POST.get("precision_type", "decimals")
            precision_value = int(request.POST.get("precision_value", 2))

        except ValueError as e:
            context["template_data"] = {
                "message_method": f"Error: {str(e)}",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "solution": [],
            }
            return self.render_to_response(context)

        # Ejecutar el método Gauss-Seidel con los parámetros recibidos
        method_response = self.method_service.solve(
            A=A,
            b=b,
            x0=x0,
            tolerance=tolerance,
            max_iterations=max_iterations,
            precision_type=precision_type,
            precision_value=precision_value,
        )

        # Si el servicio retorna un error de validación, mostrarlo en la página
        if not method_response["is_successful"]:
            context["template_data"] = method_response
            return self.render_to_response(context)

        # Verificación de éxito y almacenamiento de la respuesta
        context["template_data"] = method_response
        context["indices"] = list(range(1, matrix_size + 1))

        return self.render_to_response(context)
