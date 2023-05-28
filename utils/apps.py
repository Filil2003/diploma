from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UtilsConfig(AppConfig):
    """ Class representing a 'utils' application and its configuration. """
    name = 'utils'  # Application name corresponding to directory name.
    verbose_name = _('Utils')  # Human-readable name for the application.
