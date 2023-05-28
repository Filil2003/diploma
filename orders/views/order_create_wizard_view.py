from _decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import Form
from django.shortcuts import get_object_or_404, redirect
from formtools.wizard.views import SessionWizardView

from cleaning.models import Service
from orders import forms, models

FORMS: tuple = (
    ('appointment', forms.AppointmentForm),
    ('options', forms.OptionsForm),
    ('preview', Form)
)

TEMPLATES: dict[str, str] = {
    'appointment': 'orders/appointment.html',
    'options': 'orders/options.html',
    'preview': 'orders/preview.html'
}


class OrderCreateWizardView(LoginRequiredMixin, SessionWizardView):
    form_list: tuple = FORMS
    pattern_name: str = 'orders:create'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug: str | None = None
        self.service: Service | None = None

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step=step)
        if step == 'options':
            # Add additional data to the form.
            kwargs['extra_options'] = list(self.service.extra_options())
        return kwargs

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'preview':
            options_data = self.get_cleaned_data_for_step('options')
            extra_options = self.service.extra_options()
            selected_extra_options = []
            extra_options_price = 0
            for key, value in options_data.items():
                if value:
                    option_id = int(key.split('_')[1])
                    service_option = extra_options.get(id=option_id)
                    option_data = {
                        'option': service_option.option.title,
                        'place': service_option.place,
                        'price': service_option.price,
                        'quantity': value,
                        'unit_forms': service_option.option.get_unit_forms(),
                        'total_price': service_option.price * value,
                    }
                    extra_options_price += option_data['total_price']
                    selected_extra_options.append(option_data)
            context['appointment'] = self.get_cleaned_data_for_step('appointment')
            context['selected_extra_options'] = selected_extra_options
            context['base_price'] = self.service.base_price
            context['extra_options_price'] = extra_options_price
            context['total_price'] = extra_options_price + self.service.base_price
        return context

    def dispatch(self, request, *args, **kwargs):
        # Checking for the existence of the Service object.
        self.slug = self.kwargs.get('slug')
        service = get_object_or_404(Service, slug=self.slug)
        # Saving the Service object for future use.
        self.service = service
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def done(self, form_list, **kwargs):
        appointment = self.get_cleaned_data_for_step('appointment')
        scheduled_date = appointment.pop('scheduled_date')
        scheduled_time = appointment.pop('scheduled_time')
        address, created = models.Address.objects.get_or_create(**appointment)

        included_options = []
        for service_option in self.service.included_options():
            included_options.append({
                'title': service_option.option.title,
                'place': service_option.place.title,
            })

        total_price = 0
        extra_options = []
        service_extra_options = self.service.extra_options()
        options_data = self.get_cleaned_data_for_step('options')
        for key, value in options_data.items():
            if value:
                option_id = int(key.split('_')[1])
                service_option = service_extra_options.get(id=option_id)
                item = {
                    'title': service_option.option.title,
                    'place': service_option.place.title,
                    'price': str(service_option.price),
                    'quantity': value,
                    'total_price': str(service_option.price * value),
                }
                total_price += Decimal(item['total_price'])
                extra_options.append(item)

        order = models.Order.objects.create(
            customer=self.request.user,
            address=address,
            service_title=self.service.title,
            service_base_price=self.service.base_price,
            total_price=self.service.base_price + total_price,
            service_included_options=included_options,
            service_extra_options=extra_options,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time
        )
        self.request.session['order_id'] = order.id
        return redirect('payment:process')
