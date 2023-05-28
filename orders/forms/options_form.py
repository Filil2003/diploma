from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class OptionsForm(forms.Form):
    """
    Form for selecting extra options.

    Fields:
    - automatically_generated_option: BooleanField or IntegerField option.

    Validation:
    - IntegerField: only numbers from 0 to 25 accept.
    """

    def __init__(self, *args, **kwargs):
        """ Initialize the form. """
        # Get an extra options list from keyword arguments.
        self.extra_options = kwargs.pop('extra_options')

        # Calling the parent's constructor.
        super().__init__(*args, **kwargs)

        # Iterate over the list and create a form element for each option.
        for service_option in self.extra_options:
            # Use the option PK as the field name.
            field_name = f'option_{service_option.pk}'
            if service_option.option.type == service_option.option.TypeEnum.SWITCH:
                self.fields[field_name] = forms.BooleanField(
                    label=service_option.option.title,
                    required=False,
                    initial=False,
                    widget=forms.CheckboxInput(
                        attrs={
                            'hidden': 'hidden',
                            'data-place': service_option.place,
                            'data-price': service_option.price,
                            'data-unit': service_option.option.unit
                        }
                    )
                )
            else:
                self.fields[field_name] = forms.IntegerField(
                    label=service_option.option.title,
                    initial=0,
                    min_value=0,
                    max_value=25,
                    required=False,
                    validators=(
                        MinValueValidator(0),
                        MaxValueValidator(25)
                    ),
                    widget=forms.NumberInput(
                        attrs={
                            'readonly': '',
                            'data-place': service_option.place,
                            'data-price': service_option.price,
                            'data-unit': service_option.option.unit
                        }
                    )
                )
