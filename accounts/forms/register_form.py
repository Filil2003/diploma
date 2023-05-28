from hashlib import sha256

from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

user_model = get_user_model()


class RegisterForm(forms.Form):
    """
    A form used for registering a new user account.

    Fields:
    - email: the user email address;
    - password1: the user password;
    - password2: a confirmation of the user password.

    Validation:
    - Checks if the user does not exist yet;
    - Checks that the two entered passwords match.
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
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form__input',
                'placeholder': ' '
            }
        )
    )
    password2 = forms.CharField(
        label=_('Подтвердите пароль'),
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form__input',
                'placeholder': ' '
            }
        )
    )

    def clean_email(self) -> str:
        """
        Check the user with given 'email' does not exist.
        Raise ValidationError if user exists.
        Return email.
        """
        email: str = self.cleaned_data['email']
        token: str = sha256(email.encode()).hexdigest()
        if user_model.objects.filter(email=email).exists() or token in cache:
            self.add_error('email', _('Пользователь уже существует.'))
        return email

    def clean_password2(self) -> str:
        """ Check password match. """
        data: dict = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError(_('Пароли не совпадают.'))
        return data['password2']
