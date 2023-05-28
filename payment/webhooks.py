import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import WebhookNotification, WebhookNotificationEventType

from orders.models import Order


@csrf_exempt
def payment_notification(request):
    # Extracting JSON object from request body.
    event_json = json.loads(request.body)
    try:
        # Create an object of the notification class depending on the event.
        notification_object = WebhookNotification(event_json)
        response_object = notification_object.object
    except ValueError:
        return HttpResponse(status=400)
    if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
        order = get_object_or_404(Order, payment_id=response_object.id)
        order.payment_status = Order.PaymentStatusEnum.PAYMENT_SUCCEEDED
        order.save()
        order.customer.email_user(
            'Заказ оплачен',
            f'Заказ №{order.pk} \'{order.service_title}\' оплачен на сумму {order.total_price} рублей.'
        )
    elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
        order = get_object_or_404(Order, payment_id=response_object.payment_id)
        order.payment_status = Order.PaymentStatusEnum.REFUND_SUCCEEDED
        order.execution_status = Order.ExecutionStatusEnum.CANCELED
        order.save()
        order.customer.email_user(
            'Возврат средств',
            f'''Заказ №{order.pk} \'{order.service_title}\' отменён.\n
            Возврат средств на сумму {order.total_price} рублей.'''
        )

    return HttpResponse(status=200)
