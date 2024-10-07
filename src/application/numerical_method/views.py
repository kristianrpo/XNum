from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from .methods.SENL.bisection import bisection_method

class bisection(TemplateView):
    template_name = "bisection.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        interval_a = float(request.POST.get('interval_a'))
        interval_b = float(request.POST.get('interval_b'))
        tolerance = float(request.POST.get('tolerance'))
        max_iterations = int(request.POST.get('max_iterations'))
        function_input = request.POST.get('function_input')
        precision = int(request.POST.get('precision'))

        interval = [interval_a, interval_b]
        
        template_data = bisection_method(function_input, interval, tolerance, max_iterations, precision)
        context['template_data'] = template_data

        return self.render_to_response(context)
