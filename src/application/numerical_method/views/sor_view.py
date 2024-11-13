from django.views.generic import TemplateView
from src.application.numerical_method.containers.numerical_method_container import (
    NumericalMethodContainer,
)
from dependency_injector.wiring import inject
from django.http import HttpRequest, HttpResponse


class SORView(TemplateView):
    template_name = "sor.html"

    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.method_service = NumericalMethodContainer.sor_service()

    def post(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponse:
        context = self.get_context_data()
        template_data = {}

        try:
            # Capturar el tamaño de la matriz
            matrix_size = int(request.POST.get("matrix_size", 3))

            # Validación y conversión de la matriz A
            matrix_a_raw = request.POST.get("matrix_a", "")
            A = [
                [float(num) for num in row.strip().split()]
                for row in matrix_a_raw.split(";") if row.strip()
            ]
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

            # Validación de tolerancia y número máximo de iteraciones
            tolerance = float(request.POST.get("tolerance", 0))
            max_iterations = int(request.POST.get("max_iterations", 100))

            # Capturar el factor de relajación (w)
            w = float(request.POST.get("relaxation_factor", 1.0))
            if w <= 0 or w >= 2:
                raise ValueError("El factor de relajación w debe estar en el rango (0, 2).")

            # Validación y captura de precisión
            precision_type = request.POST.get("precision_type", "decimals")
            precision_value = int(request.POST.get("precision_value", 2))
            if precision_value <= 0:
                raise ValueError("El valor de precisión debe ser mayor que 0.")

        except ValueError as e:
            # Si hay un error en los datos ingresados, mostrar un mensaje de error
            template_data = {
                "message_method": f"Error: {str(e)}",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "solution": [],
            }
            context["template_data"] = template_data
            return self.render_to_response(context)

        # Ejecutar el método SOR con los parámetros recibidos
        method_response = self.method_service.solve(
            A=A,
            b=b,
            x0=x0,
            tolerance=tolerance,
            max_iterations=max_iterations,
            w=w,
            precision_type=precision_type,
            precision_value=precision_value,
        )

        # Si el servicio retorna un error de validación, mostrarlo en la página
        if not method_response["is_successful"]:
            context["template_data"] = method_response
            return self.render_to_response(context)

        # Verificación de éxito y almacenamiento de la respuesta
        template_data["indexes"] = list(range(1, len(A) + 1))
        template_data["relaxation_factor"] = w
        template_data = template_data | method_response
        context["template_data"] = template_data

        return self.render_to_response(context)
