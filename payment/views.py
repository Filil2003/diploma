from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from yookassa import Configuration, Payment, Refund

from orders.models import Order

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class PaymentProcessView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, *args, **kwargs):
        order_id = request.session.pop('order_id', None)
        order = Order.objects.get(id=order_id)
        if not order or order.customer != request.user or order.payment_id:
            return HttpResponseBadRequest()
        payment = Payment.create({
            'amount': {
                'value': order.total_price,
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': request.build_absolute_uri(reverse_lazy('accounts:orders'))
            },
            'capture': True,
            'description': f'Заказ \'{order.service_title}\'',
            'metadata': {
                'orderNumber': order.pk,
            }
        })
        order.payment_id = payment.id
        order.save()
        return redirect(payment.confirmation.confirmation_url, code=303)


class PaymentRefundView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        if order.payment_status == Order.PaymentStatusEnum.REFUND_SUCCEEDED:
            return redirect(reverse_lazy('accounts:orders'))
        if not order or \
                order.customer != request.user or \
                order.payment_status != Order.PaymentStatusEnum.PAYMENT_SUCCEEDED:
            return HttpResponseBadRequest()
        Refund.create({
            'amount': {
                'value': order.total_price,
                'currency': 'RUB'
            },
            'payment_id': order.payment_id
        })
        messages.success(
            request,
            f'Заказ #{order.pk} в скором времени будет отменён.',
            extra_tags='alert-info'
        )
        return redirect('accounts:orders')
