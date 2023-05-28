from django.contrib import messages
from django.contrib.auth import views
from django.urls import reverse_lazy

from accounts import forms


class PasswordResetView(views.PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = 'accounts/password_reset/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    subject_template_name = 'accounts/email/password_subject_reset_mail.txt'
    email_template_name = 'accounts/email/password_reset_email.html'


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset/password_reset_done.html'
    title = 'Письмо отправлено'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = forms.SetPasswordForm
    template_name = 'accounts/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Пароль успешно изменён',
            extra_tags='alert-success'
        )
        return super().form_valid(form)
