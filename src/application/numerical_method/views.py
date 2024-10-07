from django.views.generic import TemplateView
from src.application.numerical_method.services.bisection_service import NumericalMethodService
from .containers.numerical_method_container import NumericalMethodContainer
from dependency_injector.wiring import inject, Provide

class BisectionView(TemplateView):
    template_name = "bisection.html"

    @inject
    def __init__(self, method_service: NumericalMethodService = Provide[NumericalMethodContainer.bisection_service], **kwargs):
        super().__init__(**kwargs)
        self.method_service = method_service

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        interval_a = float(request.POST.get('interval_a'))
        interval_b = float(request.POST.get('interval_b'))
        tolerance = float(request.POST.get('tolerance'))
        max_iterations = int(request.POST.get('max_iterations'))
        function_input = request.POST.get('function_input')
        precision = int(request.POST.get('precision'))

        interval = [interval_a, interval_b]
        
        template_data = self.method_service.solve(function_input, interval, tolerance, max_iterations, precision)
        context['template_data'] = template_data

        return self.render_to_response(context)