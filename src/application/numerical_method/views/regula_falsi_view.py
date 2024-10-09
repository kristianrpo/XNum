from django.views.generic import TemplateView
from src.application.numerical_method.interfaces.numerical_method import (
    NumericalMethod,
)
from src.application.numerical_method.containers.numerical_method_container import (
    NumericalMethodContainer,
)
from dependency_injector.wiring import inject, Provide
from src.application.shared.utils.plot_function import plot_function
from django.http import HttpRequest, HttpResponse


class RegulaFalsiView(TemplateView):
    template_name = "regula_falsi.html"

    @inject
    def __init__(
        self,
        method_service: NumericalMethod = Provide[
            NumericalMethodContainer.regula_falsi_service
        ],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.method_service = method_service

    def post(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponse:
        context = self.get_context_data()

        template_data = {}

        interval_a = float(request.POST.get("interval_a"))
        interval_b = float(request.POST.get("interval_b"))
        tolerance = float(request.POST.get("tolerance"))
        max_iterations = int(request.POST.get("max_iterations"))
        function_input = request.POST.get("function_input")
        precision = int(request.POST.get("precision"))

        interval = [interval_a, interval_b]

        method_response = self.method_service.solve(
            function_input, interval, tolerance, max_iterations, precision
        )

        if method_response["is_successful"]:
            plot_function(
                function_input,
                method_response["have_solution"],
                method_response["root"],
            )

        template_data = template_data | method_response
        context["template_data"] = template_data

        return self.render_to_response(context)
