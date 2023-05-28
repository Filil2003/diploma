"""
The 'forms' package contains forms used throughout the 'accounts' app.

The following submodules included:
    - 'login_form': Contain a form used for user login;
    - 'password_reset_forms': Contain forms used for reset password;
    - 'register_form': Contain a form used for user registration.
"""

from .login_form import LoginForm
from .password_reset_forms import *
from .register_form import RegisterForm
