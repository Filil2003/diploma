from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect

from accounts.forms import LoginForm

user_model = get_user_model()


class LoginView(DjangoLoginView):
    """
    View account login page.
    Provide a page with authorization form.

    Attributes:
        template_name (str): Path to the template the view renders;
        authentication_form (LoginForm): Form class the view uses for authentication;
        extra_context (dict): Extra context data for rendering page.

    Methods:
        form_valid (): Checks if the user exists in the database;
        get_initial (): Initialise form data;
        dispatch (): Redirects authorized users.
    """
    template_name: str = 'accounts/login.html'
    authentication_form: LoginForm = LoginForm
    extra_context = {
        'title': 'Вход'
    }

    def form_valid(self, form: LoginForm):
        """ Run when the form has passed validation. """
        data: dict = form.cleaned_data

        # Try to authenticate the user.
        user: user_model | None = authenticate(
            email=data['email'],
            password=data['password']
        )

        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            messages.error(
                self.request,
                'Неверный email или пароль',
                extra_tags='alert-danger'
            )
            return self.form_invalid(form)

    def get_initial(self):
        """ Add extra initial data to the form. """
        initial: dict = super().get_initial()
        data = self.request.session.pop('form_data', None)
        if data is not None:
            initial['email'] = data['email']
            initial['password'] = data['password1']
        return initial

    def dispatch(self, request, *args, **kwargs):
        """ Run when the view call. """
        # Check if the user logged in.
        if request.user.is_authenticated:
            # Redirect authorized users.
            return redirect('cleaning:home')
        return super().dispatch(request, *args, **kwargs)
