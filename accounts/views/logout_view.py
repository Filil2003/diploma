from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy


class LogoutView(LoginRequiredMixin, DjangoLogoutView):
    """
    Account logout view.
    Logout the user and redirect to the next_page.

    Attributes:
        next_page (str): Next view handler.
    """
    next_page: str = reverse_lazy('cleaning:home')
