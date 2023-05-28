from datetime import timedelta, date

from django import forms


class AppointmentForm(forms.Form):
    """
    Form for planning the place and time of cleaning.

    Fields:
    - city: full city name;
    - street: full street name;
    - house: full house name (including building and building);
    - flat: number of the flat (optional);
    - scheduled_date: scheduled date of service;
    - scheduled_time: scheduled service time.

    Validation:
    - flat: Flat numbers from 1 to 2000 accept;
    - scheduled_time: Times from the `SCHEDULED_TIME_CHOICES` list accept;
    - scheduled_date: Dates from tomorrow to plus three weeks accept.
    """
    city: str = forms.CharField(
        label='Город',
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'placeholder': ' '
            }
        )
    )
    street: str = forms.CharField(
        label='Улица',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'placeholder': ' '
            }
        )
    )
    house: str = forms.CharField(
        label='Дом',
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'placeholder': ' '
            }
        )
    )
    flat: int = forms.IntegerField(
        label='Квартира',
        min_value=0,
        max_value=2000,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form__input',
                'placeholder': ' '
            }
        ),
        error_messages={
            'min_value': 'Номер квартиры должен быть больше 0.',
            'max_value': 'Номер квартиры должен быть меньше 2000.'
        }
    )
    scheduled_date: date = forms.DateField(
        label='Дата',
        localize=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form__input',
                'placeholder': ' ',
                'readonly': '',
                'autocomplete': 'off'
            }
        )
    )
    scheduled_time: str = forms.TimeField(
        label='Время',
        widget=forms.TimeInput(
            attrs={
                'class': 'form__input',
                'placeholder': ' ',
                'readonly': '',
                'autocomplete': 'off'
            }
        )
    )

    def clean_scheduled_date(self) -> date | None:
        """ Check if the value of `scheduled_date` field in allowed range. """
        scheduled_date: date = self.cleaned_data['scheduled_date']
        min_date: date = date.today() + timedelta(days=1)
        max_date: date = date.today() + timedelta(weeks=3)
        if min_date <= scheduled_date <= max_date:
            return scheduled_date
        else:
            self.add_error('scheduled_date', 'Выбрана недопустимая дата.')
