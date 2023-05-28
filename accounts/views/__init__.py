"""
The 'views' package contains views for handling 'accounts' views.

The following submodules included:
    - 'activate_view': Contains a view for handling user account activation;
    - 'login_view': Contains a view for handling user authentication;
    - 'logout_view': Contains a view for handling user logout;
    - 'orders_view': Contains a view for handling user orders;
    - 'register_view': Contains a view for handling user password reset.
"""

from .activate_view import ActivateView
from .login_view import LoginView
from .logout_view import LogoutView
from .orders_view import OrdersView
from .password_reset_views import *
from .register_view import RegisterView
