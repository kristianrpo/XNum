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

    def post(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponse:
        context = self.get_context_data()

        template_data = {}

        matrix_a_raw = request.POST.get("matrix_a", "")
        vector_b_raw = request.POST.get("vector_b", "")
        initial_guess_raw = request.POST.get("initial_guess", "")
        tolerance = float(request.POST.get("tolerance"))
        max_iterations = int(request.POST.get("max_iterations"))

        response_validation = self.method_service.validate_input(
            matrix_a_raw=matrix_a_raw,
            vector_b_raw=vector_b_raw,
            initial_guess_raw=initial_guess_raw,
            tolerance=tolerance,
            max_iterations=max_iterations,  
        )

        if isinstance(response_validation, str):
            error_response = {
                "message_method": response_validation,
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "solution": [],
            }
            template_data = template_data | error_response
            context["template_data"] = template_data
            return self.render_to_response(context)
        
        # Obtener los valores de A, b y x0
        A = response_validation[0]
        b = response_validation[1]
        x0 = response_validation[2]

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
        if method_response["is_successful"]:
            index = list(range(1, len(A) + 1))  # Índices de X
            method_response["index"] = index

        context["template_data"] = method_response

        return self.render_to_response(context)
