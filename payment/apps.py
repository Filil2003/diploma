from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentConfig(AppConfig):
    """ Class representing a 'payment' application and its configuration. """
    name = 'payment'  # Application name corresponding to directory name.
    verbose_name = _('Payment')  # Human-readable name for the application.
