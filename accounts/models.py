from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    """ Represents an application user. """
    email: str = models.EmailField(unique=True, max_length=255)
    password: str = models.CharField(
        max_length=128,
        blank=False,
        null=False
    )
    is_active: bool = models.BooleanField(default=True)
    is_staff: bool = models.BooleanField(default=False)
    is_superuser: bool = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects: AccountManager = AccountManager()

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list = []

    class Meta:
        verbose_name: str = _('Account')
        verbose_name_plural: str = _('Accounts')

    def get_full_name(self) -> str:
        """ Return the full email address. """
        return self.email

    def get_short_name(self) -> str:
        """ Return the email name. """
        return self.email.split('@')[0]

    def email_user(self, subject, message, **kwargs) -> None:
        """ Send the email to this user. """
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email], **kwargs)
