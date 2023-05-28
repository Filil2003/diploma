from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, View

from .models import Service


class HomeRedirectView(View):
    """ Home page redirect. """

    @staticmethod
    def get(request, *args, **kwargs):
        first_service = Service.objects.first()
        if first_service:
            return redirect(first_service.absolute_url)
        return HttpResponse(status=503)


class ServiceDetailView(DetailView):
    """ Service detail page. """
    model: Service = Service
    template_name: str = 'cleaning/service_detail.html'
    context_object_name: str = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        details = {}
        for place in self.object.places:
            included_options, extra_options = self.object.get_options_for_place(place.place.id)
            details[place] = {
                'included_options': included_options,
                'extra_options': extra_options
            }
        context['details'] = details
        return context
