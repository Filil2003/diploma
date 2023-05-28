from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    """ Class representing an 'orders' application and its configuration. """
    name = 'orders'  # Application name corresponding to directory name.
    verbose_name = _('Orders')  # Human-readable name for the application.
