from django.views.generic import TemplateView
from src.application.numerical_method.interfaces.interval_method import (
    IntervalMethod,
)
from src.application.numerical_method.containers.numerical_method_container import (
    NumericalMethodContainer,
)
from dependency_injector.wiring import inject, Provide
from src.application.shared.utils.plot_function import plot_function
from django.http import HttpRequest, HttpResponse


class BisectionView(TemplateView):
    template_name = "bisection.html"

    @inject
    def __init__(
        self,
        method_service: IntervalMethod = Provide[
            NumericalMethodContainer.bisection_service
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
        function_f = request.POST.get("function_f")
        precision = int(request.POST.get("precision"))

        response_validation = self.method_service.validate_input(
            interval_a=interval_a,
            interval_b=interval_b,
            tolerance=tolerance,
            max_iterations=max_iterations,
            function_f=function_f,
        )

        if isinstance(response_validation, str):
            error_response = {
                "message_method": response_validation,
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }
            template_data = template_data | error_response
            context["template_data"] = template_data
            return self.render_to_response(context)

        method_response = self.method_service.solve(
            interval_a=interval_a,
            interval_b=interval_b,
            tolerance=tolerance,
            max_iterations=max_iterations,
            function_f=function_f,
            precision=precision,
        )

        if method_response["is_successful"]:
            plot_function(
                function_f,
                method_response["have_solution"],
                [(method_response["root"], 0.0)],
            )

        template_data = template_data | method_response
        context["template_data"] = template_data

        return self.render_to_response(context)
