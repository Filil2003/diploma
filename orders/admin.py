from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from orders.models import Order, Address


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">Detail</a>')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'city', 'street', 'house', 'flat')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'service_title',
        'customer',
        'display_total_price',
        'execution_status',
        'display_payment_status',
        order_detail
    )
    list_filter = ('service_title', 'customer', 'execution_status', 'payment_status')

    def display_payment_status(self, obj):
        return obj.payment_status

    display_payment_status.short_description = 'Payment Status'

    def display_total_price(self, obj):
        return f'{obj.total_price}₽'

    display_total_price.short_description = 'Total price'
