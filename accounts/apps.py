from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    """ Class representing an 'accounts' application and its configuration. """
    name = 'accounts'  # Application name corresponding to directory name.
    verbose_name = _('Accounts')  # Human-readable name for the application.
