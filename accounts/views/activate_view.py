from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic import RedirectView

user_model = get_user_model()


class ActivateView(RedirectView):
    """
    Account activation view.
    Activate the user with the given activation token.
    Redirect to the login page.

    Attributes:
        pattern_name (str): The name of the URL pattern to redirect to.

    Methods:
        get (): Handle GET requests for account activation.
    """
    pattern_name = 'accounts:login'

    def get(self, request, *args, **kwargs):
        token: str = kwargs.get('token')
        if token in cache:
            data: dict = cache.get(token)
            user = data['user']
            user.save()
            cache.delete(token)
            messages.success(
                request,
                'Аккаунт успешно создан',
                extra_tags='alert-success'
            )
        else:
            messages.error(
                request,
                'Несуществующий токен',
                extra_tags='alert-danger'
            )
        return redirect(self.pattern_name)
