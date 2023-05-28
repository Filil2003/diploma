from hashlib import sha256

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import FormView

from accounts.forms import RegisterForm

user_model = get_user_model()


class RegisterView(FormView):
    """
    Account register view.
    Display the account password_reset form.
    If the data in the form passes validation,
    write the user image to the CACHE for 15 minutes.
    In other cases, display errors to the user.

    Attributes:
        template_name (str): Path to the template the view renders;
        form_class (RegisterForm): The form to use in this view;
        success_url (str): URL to redirect after successful form processing;
        extra_context (dict): Extra context data for rendering template.

    Methods:
        form_valid (): Preregister user in the CACHE;
        dispatch (): Redirects authorized users.
    """
    template_name: str = 'accounts/register.html'
    form_class: RegisterForm = RegisterForm
    success_url: str = reverse_lazy('accounts:login')
    extra_context: dict = {
        'title': 'Регистрация'
    }

    def form_valid(self, form):
        """ Run when the form has passed validation. """
        # Get necessary cleaned data.
        email: str = form.cleaned_data['email']
        password: str = form.cleaned_data['password2']

        # Create a user.
        user = user_model(email=email)
        user.set_password(password)

        # Generate hash token from email.
        token: str = sha256(email.encode()).hexdigest()

        # Save the user in CACHE for 15 minutes.
        data: dict = {
            'user': user,
            'created_at': timezone.now()
        }
        cache.set(token, data, timeout=60 * 15)

        # Asemble the user's activation url.
        scheme: str = self.request.scheme
        current_site = get_current_site(self.request)
        path: str = reverse('accounts:activate', kwargs={'token': token})
        activation_url: str = f'{scheme}://{current_site}{path}'

        # Get email template as a string.
        message = render_to_string(
            'accounts/email/activation_email.html',
            {'activation_url': activation_url}
        )

        # Send the user an email with a link to activate the account.
        user.email_user(
            subject='Подтверждение регистрации',
            message=message,
            fail_silently=False
        )

        # Add a success message.
        messages.success(
            self.request,
            'Письмо с подтверждением успешно отправлено',
            extra_tags='alert-info'
        )

        # Save the form data in the session
        self.request.session['form_data'] = form.cleaned_data

        # Redirect to the login page.
        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        """ Run when the view call. """
        # Check if the user logged in.
        if request.user.is_authenticated:
            # Redirect authorized users.
            return redirect('cleaning:home')
        return super().dispatch(request, *args, **kwargs)
