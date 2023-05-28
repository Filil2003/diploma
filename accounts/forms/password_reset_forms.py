from django.contrib.auth import forms


class PasswordResetForm(forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'autocomplete': 'email',
                'class': 'form__input',
                'placeholder': ' '
            })


class SetPasswordForm(forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'autocomplete': 'new-password',
                'class': 'form__input',
                'placeholder': ' '
            })
