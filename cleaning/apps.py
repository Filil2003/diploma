from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CleaningConfig(AppConfig):
    """ Class representing a 'cleaning' application and its configuration. """
    name = 'cleaning'  # Application name corresponding to directory name.
    verbose_name = _('Cleaning')  # Human-readable name for the application.
