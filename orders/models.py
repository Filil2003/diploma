from django.contrib.auth import get_user_model
from django.db import models

user_model = get_user_model()


class Order(models.Model):
    """ A model representing a customer order for a service. """

    class ExecutionStatusEnum(models.TextChoices):
        """ Enumerating execution statuses for the order. """
        CREATED: str = 'Created'
        CANCELED: str = 'Canceled'
        COMPLETED: str = 'Completed'

    class PaymentStatusEnum(models.TextChoices):
        """ Enumerating payment statuses for the order. """
        PAYMENT_WAITING_FOR_PAYMENT: str = 'Waiting for payment'
        PAYMENT_SUCCEEDED: str = 'Succeeded'
        PAYMENT_CANCELED: str = 'Canceled'
        REFUND_SUCCEEDED: str = 'Refunded'

    customer = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
    )
    address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    service_title = models.CharField(max_length=50)
    service_base_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_included_options = models.JSONField(default=list)
    service_extra_options = models.JSONField(default=list, blank=True)
    execution_status = models.CharField(
        max_length=20,
        choices=ExecutionStatusEnum.choices,
        default=ExecutionStatusEnum.CREATED.value
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatusEnum.choices,
        default=PaymentStatusEnum.PAYMENT_WAITING_FOR_PAYMENT.value
    )
    payment_id = models.CharField(max_length=250, blank=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self) -> str:
        return f'Order: {self.pk}'

    def calculate_total_price(self) -> None:
        """ Calculate the total price of the order. """
        options_price = sum(
            [option['total_price'] for option in self.service_extra_options.values()]
        )
        self.total_price = options_price + self.service_base_price

    @property
    def payment_url(self) -> str | None:
        """ Return the payment url for the order. """
        if self.payment_id:
            return f'https://yoomoney.ru/checkout/payments/v2/contract?orderId={self.payment_id}'


class Address(models.Model):
    """ Provide detailed address information. """
    city: str = models.CharField(
        help_text='Город',
        max_length=255
    )
    street: str = models.CharField(
        help_text='Улица',
        max_length=255
    )
    house: str = models.CharField(
        help_text='Дом',
        max_length=50
    )
    flat: str = models.CharField(
        help_text='Квартира',
        max_length=5,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        result = f'{self.city}, {self.street}, {self.house}'
        if self.flat:
            result += f', {self.flat}'
        return result
