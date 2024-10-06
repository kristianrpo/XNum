from django.shortcuts import render
from django.views.generic import TemplateView


class bisection(TemplateView):
    template_name = "numerical_method/bisection.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)
