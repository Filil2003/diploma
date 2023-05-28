from django.urls import path

from payment import views, webhooks

app_name = 'payment'

urlpatterns = (
    path('process/', views.PaymentProcessView.as_view(), name='process'),
    path('refund/<int:order_id>', views.PaymentRefundView.as_view(), name='refund'),
    path('notification/', webhooks.payment_notification, name='notification')
)
