from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

user_model = get_user_model()


class LoginForm(forms.Form):
    """
    A form for authenticating users by email and password.

    Fields:
    - email: the user email address;
    - password: the user password.

    Validation:
    - Checks if the user among the non-activated accounts.
    """
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
                'class': 'form__input',
                'placeholder': ' '
            }
        )
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'form__input',
                'placeholder': ' '
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email in cache:
            self.add_error('email', _('Проверьте почту!'))
        return email
